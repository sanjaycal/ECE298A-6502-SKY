`ifndef OPCODES
    `define OPCODES 1

    //LOAD/STORE OPCODES

    `define OP_LD_X_ZPG     8'b10100110
    `define OP_ST_X_ZPG     8'b10000110

    `define OP_LD_A_ZPG     8'b10100101
    `define OP_ST_A_ZPG     8'b10000101

    `define OP_LD_Y_ZPG     8'ha4
    `define OP_ST_Y_ZPG     8'h84


    //SHIFTING OPCODES

    `define OP_ALU_SHIFT_ZPG    8'b00000110
    `define OP_ALU_SHIFT_ZPG_X  8'b00010110
    `define OP_ALU_SHIFT_ABS    8'b00001110

    `define OP_ALU_MASK         8'b10011111

    `define OP_ASL          8'b000xxx10
    `define OP_ASL_ZPG      8'b00000110
    `define OP_ASL_A        8'b00001010
    `define OP_ASL_ABS      8'b00001110
    `define OP_ASL_ZPG_X    8'b00010110
    
    `define OP_LSR          8'b010xxx10
    `define OP_LSR_ZPG      8'b01000110
    `define OP_LSR_A        8'b01001010
    `define OP_LSR_ABS      8'b01001110
    `define OP_LSR_ZPG_X    8'b01010110

    `define OP_ROL          8'b001xxx10
    `define OP_ROL_ZPG      8'b00100110
    `define OP_ROL_A        8'b00101010
    `define OP_ROL_ABS      8'b00101110
    `define OP_ROL_ZPG_X    8'b00110110


    `define OP_ROR          8'b011xxx10
    `define OP_ROR_ZPG      8'b01100110
    `define OP_ROR_A        8'b01101010
    `define OP_ROR_ABS      8'b01101110
    `define OP_ROR_ZPG_X    8'b01110110

    `define OP_AND_ZPG      8'b00100101
    `define OP_AND_ABS      8'b00101110
    `define OP_AND_ZPG_X    8'b00110101

    `define OP_INC_ZPG      8'b11100110
    `define OP_INC_ABS      8'b11101110
    `define OP_INC_ZPG_X    8'b11110110

    `define OP_DEC_ZPG      8'b11000110
    `define OP_DEC_ABS      8'b11001110
    `define OP_DEC_ZPG_X    8'b11011110  

    `define OP_INX          8'he8
    `define OP_INY          8'hc8
    `define OP_DEX          8'hca
    `define OP_DEY          8'h88

    //TRANSFER INSTRUCTIONS
    `define OP_TAX          8'haa
    `define OP_TAY          8'ha8
    `define OP_TXA          8'h8a
    `define OP_TYA          8'h98

    //Branch instructions
    `define OP_BEQ          8'b11110000

    //Set instructions
    `define OP_SEC          8'b00111000
    `define OP_CLC          8'b00011000
    `define OP_CLV          8'b10111000

    //Compare instructions
    `define OP_CMP_ZPG      8'b11000101
    `define OP_CMP_ZPG_X    8'b11010101
    `define OP_CMP_ABS      8'b11001101

    // MISC OPCODES
    `define OP_JSR          8'b00100000
    `define OP_JMP_ABS      8'b01001100
    `define OP_NOP          8'b11101010

    // ADDRESSING
    `define ADR_ZPG         3'b001
    `define ADR_ZPG_X       3'b101
    `define ADR_ABS         3'b011
    `define ADR_A           3'b010

`endif
