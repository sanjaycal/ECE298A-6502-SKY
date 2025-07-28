`include "../inc/opcode.vh"
`include "../inc/status_register.vh"

`include "../inc/buf_instructions.vh"
`include "../inc/status_register.vh"
`include "../inc/alu_ops.vh"

`default_nettype none

module instruction_decode (
    input  wire [7:0] instruction,
    input  wire       clk,
    input  wire       clk_enable,
    input  wire       rst_n,
    input  wire       irq,
    input  wire       nmi,
    input  wire [6:0] processor_status_register_read,
    output reg [6:0] processor_status_register_write,
    output reg [7:0] processor_status_register_value,
    output reg [15:0] memory_address,  // better name for this
    output reg [1:0]    address_select, // 0 = PC, 1 = Memory Address (Remove?), 2 = ALU,
    output reg       processor_status_register_rw,
    output reg       rw, //1 for read, 0 for write
    output reg [1:0] data_buffer_enable, // 00 IDLE, 01 LOAD, 10 STORE
    output reg [1:0] input_data_latch_enable, // 00 IDLE, 01 LOAD, 10 STORE
    output reg [2:0]     pc_enable, // 11 for a secret operation :)
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
localparam S_PC_LOAD        = 4'd12;
localparam S_BRANCH_CHECK   = 4'd13;

//BUFFER OPERATIONS

reg [3:0] STATE      = S_IDLE;
reg [3:0] NEXT_STATE = S_IDLE;
reg [15:0] MEMORY_ADDRESS_INTERNAL  = 16'b0;
reg [2:0] ADDRESSING=0;
reg [7:0] OPCODE=0;
reg [7:0] INSTRUCTION=0;

always @(*) begin
    memory_address = 16'b0;
    NEXT_STATE = STATE;
    alu_enable = `NOP;
    processor_status_register_write = 7'b0;
    processor_status_register_value = 8'b0;
    address_select = 2'b00;
    processor_status_register_rw = 1;
    rw = 1;
    data_buffer_enable = `BUF_IDLE_TWO;
    input_data_latch_enable = `BUF_IDLE_TWO;
    pc_enable = 3'b000;
    accumulator_enable = `BUF_IDLE_THREE;
    stack_pointer_register_enable = `BUF_IDLE_THREE;
    index_register_X_enable = `BUF_IDLE_THREE;
    index_register_Y_enable = `BUF_IDLE_THREE;
    case(STATE)
    S_IDLE: begin
        NEXT_STATE = S_OPCODE_READ;
    end
    S_OPCODE_READ: begin
        pc_enable = `PC_INC_ONE;   // Increment Program Counter
        // In this state, we just need to increment the PC and decide where to go next.
        // The actual loading of OPCODE and ADDRESSING will happen in the clocked block below.
        if(INSTRUCTION == `OP_NOP) begin
            NEXT_STATE = S_IDLE; // NOP is a no-operation, so we just stay idle.
        end else if(INSTRUCTION == `OP_SEC) begin
	        processor_status_register_value[7] = 1;
	        processor_status_register_value[`CARRY_FLAG] = 1;
            processor_status_register_write[`CARRY_FLAG] = 1;
            NEXT_STATE = S_IDLE;
        end else if(INSTRUCTION == `OP_CLC) begin
	        processor_status_register_value[7] = 1;
	        processor_status_register_value[`CARRY_FLAG] = 0;
            processor_status_register_write[`CARRY_FLAG] = 1;
            NEXT_STATE = S_IDLE;
        end else if(INSTRUCTION == `OP_CLV) begin
	        processor_status_register_value[7] = 1;
	        processor_status_register_value[`OVERFLOW_FLAG] = 0;
            processor_status_register_write[`OVERFLOW_FLAG] = 1;
            NEXT_STATE = S_IDLE;
        end else if(INSTRUCTION == `OP_TAX) begin
            index_register_X_enable = `BUF_LOAD1_THREE;
            accumulator_enable = `BUF_STORE1_THREE;
            NEXT_STATE = S_IDLE;
        end else if(INSTRUCTION == `OP_TAY) begin
            index_register_Y_enable = `BUF_LOAD1_THREE;
            accumulator_enable = `BUF_STORE1_THREE;
            NEXT_STATE = S_IDLE;
        end else if(INSTRUCTION == `OP_TXA) begin
            index_register_X_enable = `BUF_STORE1_THREE;
            accumulator_enable = `BUF_LOAD1_THREE;
            NEXT_STATE = S_IDLE;
        end else if(INSTRUCTION == `OP_TYA) begin
            index_register_Y_enable = `BUF_STORE1_THREE;
            accumulator_enable = `BUF_LOAD1_THREE;
            NEXT_STATE = S_IDLE;
        end else if (INSTRUCTION == `OP_LD_Y_IMM || INSTRUCTION == `OP_LD_X_IMM || INSTRUCTION == `OP_LD_A_IMM 
                     || INSTRUCTION == `OP_ORA_IMM || INSTRUCTION == `OP_AND_IMM || INSTRUCTION == `OP_EOR_IMM 
                     || INSTRUCTION == `OP_ADC_IMM || INSTRUCTION[4:0] == `ADR_REL_CHECK) begin
            NEXT_STATE = S_IDL_DATA_WRITE;
        end else if(INSTRUCTION[4:2] == `ADR_A || INSTRUCTION == `OP_INX || INSTRUCTION == `OP_INY || INSTRUCTION==`OP_DEX || INSTRUCTION ==`OP_DEY) begin
            NEXT_STATE = S_ALU_FINAL;   // because this involves registers we can go straight to final
        end else if(INSTRUCTION[4:2] == `ADR_ZPG) begin
            NEXT_STATE = S_ZPG_ABS_ADR_READ;
        end else if(INSTRUCTION[4:2] == `ADR_ZPG_X) begin
            NEXT_STATE = S_IDL_ADR_WRITE;
        end else if(INSTRUCTION[4:2] == `ADR_ABS) begin
            NEXT_STATE = S_ABS_LB;
        end else begin
            NEXT_STATE = S_IDLE; // Default case, should not happen.
        end  
    end
    S_ZPG_ABS_ADR_READ: begin
        address_select = 1;
        pc_enable = `PC_INC_ONE;
        memory_address = MEMORY_ADDRESS_INTERNAL; // Puts the memory address read in adh/adl
        NEXT_STATE = S_IDL_DATA_WRITE;
    end
    S_IDL_DATA_WRITE: begin
        input_data_latch_enable = `BUF_LOAD_TWO;
        if (OPCODE == `OP_LD_Y_IMM || OPCODE == `OP_LD_X_IMM || OPCODE == `OP_LD_A_IMM || OPCODE == `OP_ORA_IMM || OPCODE == `OP_AND_IMM || OPCODE == `OP_EOR_IMM || OPCODE == `OP_ADC_IMM) begin
            pc_enable = `PC_INC_ONE;
        end
        if(ADDRESSING == `ADR_REL) begin
            NEXT_STATE = S_BRANCH_CHECK;
        end
        else begin
            NEXT_STATE = S_ALU_FINAL;
        end

    end
    S_IDL_ADR_WRITE: begin
        input_data_latch_enable = `BUF_IDLE_TWO;
        if((OPCODE & `OP_ALU_MASK) == `OP_ALU_SHIFT_ZPG_X) begin 
            NEXT_STATE = S_ALU_ADR_CALC_1;
        end   
    end
    S_ALU_FINAL: begin
        processor_status_register_rw = 0;
        //SHIFTING
        if(OPCODE == `OP_ASL_ZPG || OPCODE ==  `OP_ASL_ZPG_X || OPCODE == `OP_ASL_ABS) begin
            input_data_latch_enable = `BUF_STORE_TWO;
            alu_enable  = `ASL;
            processor_status_register_write = `CARRY_FLAG | `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_ASL_A) begin
            accumulator_enable = `BUF_STORE1_THREE;
            alu_enable = `ASL;
            processor_status_register_write = `CARRY_FLAG | `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_LSR_ZPG || OPCODE == `OP_LSR_ZPG_X || OPCODE == `OP_LSR_ABS) begin
            input_data_latch_enable = `BUF_STORE_TWO;
            alu_enable  = `LSR;
            processor_status_register_write = `CARRY_FLAG | `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_LSR_A ) begin
            accumulator_enable = `BUF_STORE1_THREE;
            alu_enable = `LSR;
            processor_status_register_write = `CARRY_FLAG | `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_ROL_A ) begin
            accumulator_enable = `BUF_STORE1_THREE;
            alu_enable = `ROL;
            processor_status_register_write = `CARRY_FLAG | `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_ROR_A ) begin
            accumulator_enable = `BUF_STORE1_THREE;
            alu_enable = `ROR;
            processor_status_register_write = `CARRY_FLAG | `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_ROL_ZPG || OPCODE == `OP_ROL_ZPG_X || OPCODE == `OP_ROL_ABS) begin
            input_data_latch_enable = `BUF_STORE_TWO;
            alu_enable = `ROL;
            processor_status_register_write = `CARRY_FLAG | `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_ROR_ZPG || OPCODE == `OP_ROR_ZPG_X || OPCODE == `OP_ROR_ABS) begin
            input_data_latch_enable = `BUF_STORE_TWO;
            alu_enable = `ROR;
            processor_status_register_write = `CARRY_FLAG | `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_AND_ZPG || OPCODE == `OP_AND_IMM || OPCODE == `OP_AND_ABS) begin
            input_data_latch_enable = `BUF_STORE_TWO;
            accumulator_enable = `BUF_STORE2_THREE;
            alu_enable = `AND;
            processor_status_register_write = `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_ORA_ZPG || OPCODE == `OP_ORA_ABS || OPCODE == `OP_ORA_IMM) begin
            input_data_latch_enable = `BUF_STORE_TWO;
            accumulator_enable = `BUF_STORE2_THREE;
            alu_enable = `OR;
            processor_status_register_write = `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_EOR_ZPG || OPCODE == `OP_EOR_ZPG) begin
            input_data_latch_enable = `BUF_STORE_TWO;
            accumulator_enable = `BUF_STORE2_THREE;
            alu_enable = `XOR;
            processor_status_register_write = `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_ADC_ZPG || OPCODE == `OP_ADC_IMM) begin
            input_data_latch_enable = `BUF_STORE_TWO;
            accumulator_enable = `BUF_STORE2_THREE;
            alu_enable = `ADD;
            processor_status_register_write = `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_SBC_ZPG) begin
            input_data_latch_enable = `BUF_STORE_TWO;
            accumulator_enable = `BUF_STORE2_THREE;
            alu_enable = `SUB;
            processor_status_register_write = `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_CMP_ZPG || OPCODE == `OP_CMP_ZPG_X || OPCODE == `OP_CMP_ABS) begin
            input_data_latch_enable = `BUF_STORE_TWO;
            accumulator_enable = `BUF_STORE2_THREE;
            alu_enable = `CMP;
            processor_status_register_write = `ZERO_FLAG | `NEGATIVE_FLAG | `CARRY_FLAG;
        end else if(OPCODE == `OP_INC_ZPG || OPCODE == `OP_INC_ZPG_X || OPCODE == `OP_INC_ABS) begin
            input_data_latch_enable = `BUF_STORE_TWO;
            alu_enable = `INC;
            processor_status_register_write = `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_INX) begin
	    index_register_X_enable = `BUF_STORE1_THREE;
            alu_enable = `INC;
            processor_status_register_write = `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_INY) begin
	    index_register_Y_enable = `BUF_STORE1_THREE;
            alu_enable = `INC;
            processor_status_register_write = `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_DEX) begin
	    index_register_X_enable = `BUF_STORE1_THREE;
            alu_enable = `DEC;
            processor_status_register_write = `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_DEY) begin
	    index_register_Y_enable = `BUF_STORE1_THREE;
            alu_enable = `DEC;
            processor_status_register_write = `ZERO_FLAG | `NEGATIVE_FLAG;
        end else if(OPCODE == `OP_DEC_ZPG || OPCODE == `OP_DEC_ZPG_X || OPCODE == `OP_DEC_ABS) begin
                input_data_latch_enable = `BUF_STORE_TWO;
                alu_enable = `DEC;
                processor_status_register_write = `ZERO_FLAG | `NEGATIVE_FLAG;
        end 
        
        // LOAD
        else if(OPCODE == `OP_LD_X_ZPG || OPCODE==`OP_LD_A_ZPG || OPCODE==`OP_LD_Y_ZPG || 
                OPCODE == `OP_LD_Y_ABS || OPCODE == `OP_LD_A_ABS || 
                OPCODE == `OP_LD_Y_IMM || OPCODE == `OP_LD_X_IMM || OPCODE == `OP_LD_A_IMM) begin
            input_data_latch_enable = `BUF_STORE_TWO;
            alu_enable = `FLG;
            processor_status_register_write = `ZERO_FLAG | `NEGATIVE_FLAG;
        end
        NEXT_STATE = S_ALU_TMX;
    end
    S_ALU_TMX: begin
        if(OPCODE == `OP_LD_X_ZPG || OPCODE == `OP_LD_X_IMM) begin
            index_register_X_enable = `BUF_LOAD2_THREE;
            NEXT_STATE = S_IDLE;
            alu_enable = `TMX;
        end
        else if(OPCODE == `OP_LD_Y_ZPG || OPCODE == `OP_LD_Y_ABS || OPCODE == `OP_LD_Y_IMM) begin
            index_register_Y_enable = `BUF_LOAD2_THREE;
            NEXT_STATE = S_IDLE;
            alu_enable = `TMX;
        end
        else if(OPCODE == `OP_LD_A_ZPG || OPCODE == `OP_LD_A_ABS || OPCODE == `OP_LD_A_IMM ) begin
            accumulator_enable = `BUF_LOAD2_THREE;
            NEXT_STATE = S_IDLE;
            alu_enable = `TMX;
        end
        else if(
            OPCODE == `OP_AND_ZPG || 
            OPCODE == `OP_ORA_ZPG || 
            OPCODE == `OP_ORA_ABS ||
            OPCODE == `OP_EOR_ZPG || 
            OPCODE == `OP_ADC_ZPG || 
            OPCODE == `OP_SBC_ZPG ||
            OPCODE == `OP_AND_IMM || 
            OPCODE == `OP_ORA_IMM || 
            OPCODE == `OP_EOR_IMM || 
            OPCODE == `OP_ADC_IMM 
        ) begin
            accumulator_enable = `BUF_LOAD2_THREE;
            NEXT_STATE = S_IDLE;
            alu_enable = `TMX;
        end 
        else if(OPCODE == `OP_ST_X_ZPG) begin
            index_register_X_enable = `BUF_STORE2_THREE;
            data_buffer_enable = `BUF_LOAD_TWO;
            NEXT_STATE = S_DBUF_OUTPUT;
        end
        else if(OPCODE == `OP_ST_Y_ZPG) begin
            index_register_Y_enable = `BUF_STORE2_THREE;
            data_buffer_enable = `BUF_LOAD_TWO;
            NEXT_STATE = S_DBUF_OUTPUT;
        end
        else if(OPCODE == `OP_ST_A_ZPG || OPCODE == `OP_ST_A_ABS) begin
            accumulator_enable = `BUF_STORE2_THREE;
            data_buffer_enable = `BUF_LOAD_TWO;
            NEXT_STATE = S_DBUF_OUTPUT;
        end
	else if(OPCODE == `OP_INX || OPCODE == `OP_DEX) begin
	    index_register_X_enable = `BUF_LOAD2_THREE;
            alu_enable = `TMX;
	    NEXT_STATE = S_IDLE;
	end
	else if(OPCODE == `OP_INY || OPCODE == `OP_DEY) begin
	    index_register_Y_enable = `BUF_LOAD2_THREE;
            alu_enable = `TMX;
	    NEXT_STATE = S_IDLE;
	end
        else if(ADDRESSING == `ADR_ZPG || ADDRESSING == `ADR_ZPG_X || ADDRESSING == `ADR_ABS) begin
            data_buffer_enable = `BUF_LOAD_TWO;
            NEXT_STATE = S_DBUF_OUTPUT;
            alu_enable = `TMX;
        end else if(ADDRESSING == `ADR_A) begin
            accumulator_enable = `BUF_LOAD2_THREE;
            alu_enable = `TMX;
	    NEXT_STATE = S_IDLE;
        end
    end 
    S_DBUF_OUTPUT: begin
        data_buffer_enable = `BUF_STORE_TWO;
        memory_address = MEMORY_ADDRESS_INTERNAL;
        address_select = 2'd1;
        rw = 0;
        NEXT_STATE = S_IDLE;
    end
    S_ALU_ADR_CALC_1:  begin
        alu_enable  = `ADD;
        if((OPCODE & `OP_ALU_MASK) == `OP_ALU_SHIFT_ZPG_X) begin
            input_data_latch_enable = `BUF_STORE_TWO;
            index_register_X_enable = `BUF_STORE2_THREE;
        end
        NEXT_STATE = S_ALU_ADR_CALC_2;
    end
    S_ALU_ADR_CALC_2: begin
        alu_enable = `TMX;
        if((OPCODE & `OP_ALU_MASK) == `OP_ALU_SHIFT_ZPG_X) begin
            address_select = 2'd2;
            NEXT_STATE = S_IDL_DATA_WRITE;
        end
    end
    S_ABS_LB: begin
        pc_enable = `PC_INC_ONE;
        if(OPCODE == `OP_JMP_ABS) begin
            NEXT_STATE = S_PC_LOAD;
        end
        else begin
            NEXT_STATE = S_ABS_HB;
        end
    end
    S_ABS_HB: begin
        pc_enable = `PC_INC_ONE;
        memory_address = MEMORY_ADDRESS_INTERNAL; // Puts the memory address read in adh/adl
        address_select = 1;
        NEXT_STATE = S_IDL_DATA_WRITE;
    end
    S_PC_LOAD: begin
        pc_enable = `BUF_LOAD1_THREE;
        NEXT_STATE = S_IDLE;
        memory_address = MEMORY_ADDRESS_INTERNAL;
    end
    S_BRANCH_CHECK: begin
        if(OPCODE == `OP_BCS && processor_status_register_read[`CARRY_FLAG] == 1) begin
            input_data_latch_enable = `BUF_STORE_TWO;
            pc_enable = `PC_TAKE_BRANCH;
        end
        NEXT_STATE = S_IDLE;
    end
    default: NEXT_STATE = S_IDLE;
    endcase
end

always @(posedge clk or negedge rst_n) begin
    if(!rst_n) begin
        STATE <= S_IDLE;
        OPCODE <= `OP_NOP;
        ADDRESSING <= 3'b000;
        MEMORY_ADDRESS_INTERNAL <= 0;
    	INSTRUCTION <= 0;
    end else if(clk_enable) begin
	INSTRUCTION <= instruction;
        STATE <= NEXT_STATE;
        if(NEXT_STATE == S_OPCODE_READ) begin
             OPCODE <= instruction;
            if(instruction[4:0] == `ADR_REL_CHECK) begin
                ADDRESSING <= `ADR_REL;
            end else if(instruction[4:2] == `ADR_ZPG) begin
                ADDRESSING <= `ADR_ZPG;
            end else if(instruction[4:2] == `ADR_ABS) begin
                ADDRESSING <= `ADR_ABS; // THIS DOES NOT HANDLE JUMP SUBROUTINE (JSR). THAT WILL NEED ITS OWN STATES IN THE SM!!!!
            end else if(instruction[4:2] == `ADR_A) begin
                ADDRESSING <= `ADR_A;
            end else if (instruction[4:2] == `ADR_ZPG_X) begin
                ADDRESSING <= `ADR_ZPG_X;
            end
        end else if(NEXT_STATE == S_ABS_LB || NEXT_STATE == S_ZPG_ABS_ADR_READ) begin
            MEMORY_ADDRESS_INTERNAL <= {8'h00, instruction};
        end else if(NEXT_STATE == S_ABS_HB || NEXT_STATE == S_PC_LOAD) begin
            MEMORY_ADDRESS_INTERNAL <= {instruction, MEMORY_ADDRESS_INTERNAL[7:0]};
        end
    end
end

wire _unused = &{irq, nmi};

endmodule
