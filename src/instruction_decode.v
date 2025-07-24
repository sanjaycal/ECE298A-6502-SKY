`include "../inc/opcode.vh"
`include "../inc/status_register.vh"

`include "../inc/buf_instructions.vh"

`include "../inc/alu_ops.vh"

`default_nettype none

module instruction_decode (
    input  wire [7:0] instruction,
    input  wire       clk,
    input  wire       clk_enable,
    input  wire       res,
    input  wire       irq,
    input  wire       nmi,
    input  wire       rdy,
    input  wire [6:0] processor_status_register_read,
    output reg [6:0] processor_status_register_write,
    output reg [15:0] memory_address,  // better name for this
    output reg [1:0]    address_select, // 0 = PC, 1 = Memory Address (Remove?), 2 = ALU,
    output reg       processor_status_register_rw,
    output reg       rw, //1 for read, 0 for write
    output reg [1:0] data_buffer_enable, // 00 IDLE, 01 LOAD, 10 STORE
    output reg [1:0] input_data_latch_enable, // 00 IDLE, 01 LOAD, 10 STORE
    output reg       pc_enable,
    output reg [4:0] alu_enable,
    output reg [2:0] accumulator_enable, // BIT 2 is enable, BIT 1 is R/W_n and BIT 0 is BUS SELECT
    output reg [2:0] stack_pointer_register_enable, // 0 is light blue and 1 is dark blue.
    output reg [2:0] index_register_X_enable,
    output reg [2:0] index_register_Y_enable
);
//STATES

localparam S_IDLE           = 4'd0;
localparam S_OPCODE_READ    = 4'd1;
localparam S_ZPG_ABS_ADR_READ   = 4'd2;
localparam S_IDL_DATA_WRITE = 4'd3;
localparam S_IDL_ADR_WRITE  = 4'd4;
localparam S_ALU_FINAL      = 4'd5; // Final implies that there isn't anymore branching between this state and OPCODE_READ
localparam S_DBUF_OUTPUT    = 4'd6;
localparam S_ALU_TMX        = 4'd7;
localparam S_ALU_ADR_CALC_1 = 4'd8;
localparam S_ALU_ADR_CALC_2 = 4'd9;
localparam S_ABS_LB         = 4'd10;
localparam S_ABS_HB         = 4'd11;

//BUFFER OPERATIONS

reg [3:0] STATE      = S_IDLE;
//reg [3:0] NEXT_STATE = S_IDLE;
reg [15:0] MEMORY_ADDRESS_INTERNAL  = 16'b0;
reg [2:0] ADDRESSING=0;
reg [7:0] OPCODE=0;
reg [7:0] INSTRUCTION=0;

// intermediate variables

    //wire is_shift_rotate_op;
    //wire [2:0] addr_mode_bits;
    //wire is_target_addr_mode;

    //assign is_shift_rotate_op = (OPCODE[1:0] == 2'b10);
    //assign addr_mode_bits = OPCODE[4:2];
    //assign is_target_addr_mode = ((addr_mode_bits == `ADR_ZPG) ||
    //                            (addr_mode_bits == `ADR_ABS)  ||
    //                            (addr_mode_bits == `ADR_ZPG_X));

always @(posedge clk) begin
    if(clk_enable) begin
    INSTRUCTION <= instruction;
    if(res | !rdy) begin
        STATE <= S_IDLE;
        OPCODE <= `OP_NOP;
        ADDRESSING <= 3'b000;
        MEMORY_ADDRESS_INTERNAL <= 0;
    end else if(rdy) begin
        address_select <= 0;
        pc_enable <= 0;
        memory_address <= 16'b0;
        rw <= 1;
        alu_enable <= `NOP;
        processor_status_register_write <= 7'b0;
        processor_status_register_rw <= 1;
        data_buffer_enable <= `BUF_IDLE_TWO;
        input_data_latch_enable <= `BUF_IDLE_TWO;
        accumulator_enable <= `BUF_IDLE_THREE;
        stack_pointer_register_enable <= `BUF_IDLE_THREE;
        index_register_X_enable <= `BUF_IDLE_THREE;
        index_register_Y_enable <= `BUF_IDLE_THREE;
        case(STATE)
        S_IDLE: begin
            STATE <= S_OPCODE_READ;
            pc_enable <= 1;
            OPCODE <= instruction;
            if(instruction[4:2] == `ADR_ZPG) begin
                ADDRESSING <= `ADR_ZPG;
            end else if(instruction[4:2] == `ADR_ABS) begin
                ADDRESSING <= `ADR_ABS; // THIS DOES NOT HANDLE JUMP SUBROUTINE (JSR). THAT WILL NEED ITS OWN STATES IN THE SM!!!!
            end else if(instruction[4:2] == `ADR_A) begin
                ADDRESSING <= `ADR_A;
            end else if (instruction[4:2] == `ADR_ZPG_X) begin
                ADDRESSING <= `ADR_ZPG_X;
            end
        end
        S_OPCODE_READ: begin
            // In this state, we just need to increment the PC and decide where to go next.
            // The actual loading of OPCODE and ADDRESSING will happen in the clocked block below.
            if(INSTRUCTION == `OP_NOP) begin
                STATE <= S_IDLE; // NOP is a no-operation, so we just stay idle.
            end else if(INSTRUCTION[4:2] == `ADR_ZPG || INSTRUCTION == `OP_LD_Y_ZPG || INSTRUCTION == `OP_ST_Y_ZPG) begin
                STATE <= S_ZPG_ABS_ADR_READ;
                address_select <= 1;
                pc_enable <= 1;
                MEMORY_ADDRESS_INTERNAL <= {8'h00, instruction};
                memory_address <= {8'h00, instruction};
            end else if(INSTRUCTION[4:2] == `ADR_ZPG_X) begin
                STATE <= S_IDL_ADR_WRITE;
                input_data_latch_enable <= `BUF_IDLE_TWO;
            end else if(INSTRUCTION[4:2] == `ADR_ABS) begin
                STATE <= S_ABS_LB;
                pc_enable <= 1;
                MEMORY_ADDRESS_INTERNAL <= {8'h00, instruction};
            end else if(INSTRUCTION[4:2] == `ADR_A) begin
                STATE <= S_ALU_FINAL;   // because this involves registers we can go straight to final
            end else begin
                STATE <= S_IDLE; // Default case, should not happen.
            end
        end
        S_ZPG_ABS_ADR_READ: begin
            STATE <= S_IDL_DATA_WRITE;
            input_data_latch_enable <= `BUF_LOAD_TWO;
        end
        S_IDL_DATA_WRITE: begin
            STATE <= S_ALU_FINAL;
            processor_status_register_rw <= 0;
            if(OPCODE == `OP_ASL_ZPG || OPCODE ==  `OP_ASL_ZPG_X || OPCODE == `OP_ASL_ABS) begin
                input_data_latch_enable <= `BUF_STORE_TWO;
                alu_enable  <= `ASL;
                processor_status_register_write <= `CARRY_FLAG | `ZERO_FLAG | `NEGATIVE_FLAG;
            end else if(OPCODE == `OP_ASL_A) begin
                accumulator_enable <= `BUF_STORE2_THREE;
                alu_enable <= `ASL;
                processor_status_register_write <= `CARRY_FLAG | `ZERO_FLAG | `NEGATIVE_FLAG;
            end else if(OPCODE == `OP_LSR_ZPG || OPCODE == `OP_LSR_ZPG_X || OPCODE == `OP_LSR_ABS) begin
                input_data_latch_enable <= `BUF_STORE_TWO;
                alu_enable  <= `LSR;
                processor_status_register_write <= `CARRY_FLAG | `ZERO_FLAG | `NEGATIVE_FLAG;
            end else if(OPCODE == `OP_LSR_A ) begin
                accumulator_enable <= `BUF_STORE2_THREE;
                alu_enable <= `LSR;
                processor_status_register_write <= `CARRY_FLAG | `ZERO_FLAG | `NEGATIVE_FLAG;
            end else if(OPCODE == `OP_ROL_ZPG || OPCODE == `OP_ROL_ZPG_X || OPCODE == `OP_ROL_ABS) begin
                input_data_latch_enable <= `BUF_STORE_TWO;
                alu_enable <= `ROL;
                processor_status_register_write <= `CARRY_FLAG | `ZERO_FLAG | `NEGATIVE_FLAG;
            end else if(OPCODE == `OP_ROR_ZPG || OPCODE == `OP_ROR_ZPG_X || OPCODE == `OP_ROR_ABS) begin
                input_data_latch_enable <= `BUF_STORE_TWO;
                alu_enable <= `ROR;
                processor_status_register_write <= `CARRY_FLAG | `ZERO_FLAG | `NEGATIVE_FLAG;
            end else if(OPCODE == `OP_AND_ZPG || OPCODE == `OP_AND_ZPG_X || OPCODE == `OP_AND_ABS) begin
                input_data_latch_enable <= `BUF_STORE_TWO;
                accumulator_enable <= `BUF_STORE2_THREE;
                alu_enable <= `AND;
                processor_status_register_write <= `ZERO_FLAG | `NEGATIVE_FLAG;
            end else if(OPCODE == `OP_INC_ZPG || OPCODE == `OP_INC_ZPG_X || OPCODE == `OP_INC_ABS) begin
                input_data_latch_enable <= `BUF_STORE_TWO;
                alu_enable <= `INC;
                processor_status_register_write <= `ZERO_FLAG | `NEGATIVE_FLAG;
            end else if(OPCODE == `OP_DEC_ZPG || OPCODE == `OP_DEC_ZPG_X || OPCODE == `OP_DEC_ABS) begin
                input_data_latch_enable <= `BUF_STORE_TWO;
                alu_enable <= `DEC;
                processor_status_register_write <= `ZERO_FLAG | `NEGATIVE_FLAG;
            end
            // LOAD
            else if(OPCODE == `OP_LD_X_ZPG || OPCODE==`OP_LD_A_ZPG || OPCODE==`OP_LD_Y_ZPG) begin
                input_data_latch_enable <= `BUF_STORE_TWO;
                alu_enable <= `FLG;
                processor_status_register_write <= `ZERO_FLAG | `NEGATIVE_FLAG;
            end
        end
        S_IDL_ADR_WRITE: begin
            STATE <= S_ALU_ADR_CALC_1;
            alu_enable  <= `ADD;
            input_data_latch_enable <= `BUF_STORE_TWO;
            index_register_X_enable <= `BUF_STORE2_THREE;
        end
        S_ALU_FINAL: begin
            //SHIFTING
            STATE <= S_ALU_TMX;
            if(OPCODE == `OP_LD_X_ZPG) begin
                index_register_X_enable <= `BUF_LOAD2_THREE;
                alu_enable <= `TMX;
            end
            else if(OPCODE == `OP_LD_Y_ZPG) begin
                index_register_Y_enable <= `BUF_LOAD2_THREE;
                alu_enable <= `TMX;
            end
            else if(OPCODE == `OP_LD_A_ZPG) begin
                accumulator_enable <= `BUF_LOAD2_THREE;
                alu_enable <= `TMX;
            end
            else if(OPCODE == `OP_AND_ZPG) begin
                accumulator_enable <= `BUF_LOAD2_THREE;
                alu_enable <= `TMX;
            end
            else if(OPCODE == `OP_ST_X_ZPG) begin
                index_register_X_enable <= `BUF_STORE2_THREE;
                data_buffer_enable <= `BUF_LOAD_TWO;
            end
            else if(OPCODE == `OP_ST_Y_ZPG) begin
                index_register_Y_enable <= `BUF_STORE2_THREE;
                data_buffer_enable <= `BUF_LOAD_TWO;         
            end
            else if(OPCODE == `OP_ST_A_ZPG) begin
                accumulator_enable <= `BUF_STORE2_THREE;
                data_buffer_enable <= `BUF_LOAD_TWO;
            end
            else if(ADDRESSING == `ADR_ZPG || ADDRESSING == `ADR_ZPG_X || ADDRESSING == `ADR_ABS) begin
                data_buffer_enable <= `BUF_LOAD_TWO;
                alu_enable <= `TMX;
            end
            else if(ADDRESSING == `ADR_A) begin
                accumulator_enable <= `BUF_LOAD2_THREE;
                alu_enable <= `TMX;
            end
        end
        S_ALU_TMX: begin
            if(OPCODE == `OP_LD_X_ZPG) begin
                STATE <= S_OPCODE_READ;
            end
            else if(OPCODE == `OP_LD_Y_ZPG) begin
                STATE <= S_OPCODE_READ;
            end
            else if(OPCODE == `OP_LD_A_ZPG) begin
                STATE <= S_OPCODE_READ;
            end
            else if(OPCODE == `OP_AND_ZPG) begin
                STATE <= S_OPCODE_READ;
            end
            else if(OPCODE == `OP_ST_X_ZPG) begin
                STATE <= S_DBUF_OUTPUT;
                rw <= 0;
                data_buffer_enable <= `BUF_STORE_TWO;
                address_select <= 2'd1;
                memory_address <= MEMORY_ADDRESS_INTERNAL;
            end
            else if(OPCODE == `OP_ST_Y_ZPG) begin
                STATE <= S_DBUF_OUTPUT;
                rw <= 0;
                data_buffer_enable <= `BUF_STORE_TWO;
                address_select <= 2'd1;
                memory_address <= MEMORY_ADDRESS_INTERNAL;
            end
            else if(OPCODE == `OP_ST_A_ZPG) begin
                STATE <= S_DBUF_OUTPUT;
                rw <= 0;
                data_buffer_enable <= `BUF_STORE_TWO;
                address_select <= 2'd1;
                memory_address <= MEMORY_ADDRESS_INTERNAL;
            end
            else if(ADDRESSING == `ADR_ZPG || ADDRESSING == `ADR_ZPG_X || ADDRESSING == `ADR_ABS) begin
                STATE <= S_DBUF_OUTPUT;
                rw <= 0;
                data_buffer_enable <= `BUF_STORE_TWO;
                address_select <= 2'd1;
                memory_address <= MEMORY_ADDRESS_INTERNAL;
            end else if(ADDRESSING == `ADR_A) begin
                STATE <= S_OPCODE_READ;
            end
        end
        S_DBUF_OUTPUT: begin
            STATE <= S_IDLE;
        end
        S_ALU_ADR_CALC_1:  begin
            STATE <= S_ALU_ADR_CALC_2;
            alu_enable <= `TMX;
            address_select <= 2'd2;
        end
        S_ALU_ADR_CALC_2: begin
            STATE <= S_IDL_DATA_WRITE;
            input_data_latch_enable <= `BUF_LOAD_TWO;
        end
        S_ABS_LB: begin
            STATE <= S_ABS_HB;
            address_select <= 1;
            pc_enable <= 1;
            MEMORY_ADDRESS_INTERNAL <= {instruction, MEMORY_ADDRESS_INTERNAL[7:0]};
            memory_address <= {instruction, MEMORY_ADDRESS_INTERNAL[7:0]};
        end
        S_ABS_HB: begin
            STATE <= S_IDL_DATA_WRITE;
            input_data_latch_enable <= `BUF_LOAD_TWO;
        end
        default: begin
            STATE <= S_IDLE;
        end
        endcase

    end
end
end

wire _unused = &{irq, nmi, processor_status_register_read};

endmodule
