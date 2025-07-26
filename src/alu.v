`include "../inc/alu_ops.vh"
`include "../inc/status_register.vh"

`default_nettype none

module alu (
    input  wire         clk, 
    input  wire [4:0]   alu_op,
    input  wire [7:0]   inputA,
    input  wire [7:0]   inputB,
    input  wire [6:0]   status_flags_in,
    output reg  [7:0]   ALU_output,
    output reg  [6:0]   ALU_flags_output  
);

    // These calculate the result for every possible operation, all the time.
    wire [7:0] result_asl = inputA << 1;
    wire [7:0] result_lsr = inputA >> 1;
    wire [7:0] result_rol = {inputA[6:0], inputA[7]};
    wire [7:0] result_ror = {inputA[0],inputA[7:1]};
    wire [7:0] result_and = inputA&inputB;
    wire [7:0] result_or  = inputA|inputB;
    wire [7:0] result_xor = inputA^inputB;
    wire [7:0] result_inc = inputA+1;
    wire [7:0] result_dec = inputA-1;
    wire [7:0] result_cmp = inputB-inputA;

    wire [6:0] ALU_flags_output_internal = next_alu_flags;

    reg [7:0] next_alu_result = 8'b0;
    reg [6:0] next_alu_flags = 7'b0;
    always @(*) begin
        next_alu_flags = 7'b0;
        case(alu_op)
            `ASL: begin
                next_alu_result = result_asl;
                next_alu_flags[`CARRY_FLAG]    = inputA[7];
                next_alu_flags[`ZERO_FLAG]     = (result_asl == 8'b0);
                next_alu_flags[`NEGATIVE_FLAG] = result_asl[7];
            end
            `LSR: begin
                next_alu_result = result_lsr;
                next_alu_flags[`CARRY_FLAG]    = inputA[0];
                next_alu_flags[`ZERO_FLAG]     = (result_lsr == 8'b0);
                next_alu_flags[`NEGATIVE_FLAG] = result_lsr[7];  // This is physically impossible but apparently they set it like that so whatever.
            end
            `ROL: begin
                next_alu_result = result_rol;
                next_alu_flags[`CARRY_FLAG]    = inputA[7];
                next_alu_flags[`ZERO_FLAG]     = (result_rol == 8'b0);
                next_alu_flags[`NEGATIVE_FLAG] = result_rol[7];
            end
            `ROR: begin
                next_alu_result = result_ror;
                next_alu_flags[`CARRY_FLAG]    = inputA[0];
                next_alu_flags[`ZERO_FLAG]     = (result_ror == 8'b0);
                next_alu_flags[`NEGATIVE_FLAG] = result_ror[7];
            end
            `AND: begin
                next_alu_result = result_and;
                next_alu_flags[`ZERO_FLAG]     = (result_and == 8'b0);
                next_alu_flags[`NEGATIVE_FLAG] = result_and[7];
            end
            `OR: begin
                next_alu_result = result_or;
                next_alu_flags[`ZERO_FLAG]     = (result_or == 8'b0);
                next_alu_flags[`NEGATIVE_FLAG] = result_or[7];
            end
            `XOR: begin
                next_alu_result = result_xor;
                next_alu_flags[`ZERO_FLAG]     = (result_xor == 8'b0);
                next_alu_flags[`NEGATIVE_FLAG] = result_xor[7];       
            end      
            `INC: begin
                next_alu_result = result_inc;
                next_alu_flags[`ZERO_FLAG]     = (result_inc == 8'b0);
                next_alu_flags[`NEGATIVE_FLAG] = result_inc[7];
            end
            `DEC: begin
                next_alu_result = result_dec;
                next_alu_flags[`ZERO_FLAG]     = (result_dec == 8'b0);
                next_alu_flags[`NEGATIVE_FLAG] = result_dec[7];
            end
            `CMP: begin
                next_alu_result = inputA;
                next_alu_flags[`ZERO_FLAG]     = (inputB-inputA)==0;
                next_alu_flags[`NEGATIVE_FLAG] = result_cmp[7];
                next_alu_flags[`CARRY_FLAG] = (inputA[7] ^ inputB[7]) & (inputA[7] ^ result_cmp[7]);
            end
            `FLG: begin
                next_alu_result = inputA;
                next_alu_flags[`ZERO_FLAG]     = (inputA == 8'b0);
                next_alu_flags[`NEGATIVE_FLAG] = inputA[7];
            end
            // If need be add a condition that checks for tmx
            default: begin
                next_alu_result = 8'b0;
                next_alu_flags = 7'b0;
            end
        endcase
    end


    always @(posedge clk) begin
        ALU_output <= next_alu_result;
        ALU_flags_output <= ALU_flags_output_internal;
    end


    wire _unused = &{status_flags_in, result_cmp[6:0]};

endmodule
