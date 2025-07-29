`ifndef OPCODES
    `define OPCODES 1

    //LOAD OPCODES

    `define OP_LD_X_ZPG     8'b10100110
    `define OP_LD_X_IMM     8'b10100010
    `define OP_LD_X_ABS     8'hae

    `define OP_LD_A_ZPG     8'b10100101
    `define OP_LD_A_IMM     8'ha9
    `define OP_LD_A_ABS     8'had

    `define OP_LD_Y_ZPG     8'ha4
    `define OP_LD_Y_IMM     8'b10100000
    `define OP_LD_Y_ABS     8'b10101100

    //STORE OPCODES

    `define OP_ST_X_ZPG     8'b10000110
    `define OP_ST_X_ABS     8'h8e
    
    `define OP_ST_A_ZPG     8'b10000101
    `define OP_ST_A_ABS     8'h8d

    `define OP_ST_Y_ZPG     8'h84
    `define OP_ST_Y_ABS     8'h8c

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
    `define OP_AND_ABS      8'h2d
    `define OP_AND_IMM      8'h29
    `define OP_AND_ZPG_X    8'b00110101

    `define OP_ORA_ZPG      8'b00000101
    `define OP_ORA_IMM      8'h09
    `define OP_ORA_ABS      8'h0d

    `define OP_EOR_ZPG      8'b01000101
    `define OP_EOR_ABS      8'h4d
    `define OP_EOR_IMM      8'h49

    `define OP_ADC_ZPG      8'b01100101
    `define OP_ADC_ABS      8'h6d
    `define OP_ADC_IMM      8'h69

    `define OP_SBC_ZPG      8'he5
    `define OP_SBC_ABS      8'hed

    `define OP_INC_ZPG      8'b11100110
    `define OP_INC_ABS      8'hee
    `define OP_INC_ZPG_X    8'b11110110

    `define OP_DEC_ZPG      8'b11000110
    `define OP_DEC_ABS      8'hce
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
    `define OP_BCS          8'b10110000
    `define OP_BCC          8'b10010000
    `define OP_BPL          8'b00010000
    `define OP_BMI          8'b00110000
    `define OP_BEQ          8'b11110000
    `define OP_BNE          8'b11010000

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
    `define ADR_REL_CHECK   5'b10000
    `define ADR_REL         3'b111
    `define ADR_ZPG         3'b001
    `define ADR_ZPG_X       3'b101
    `define ADR_ABS         3'b011
    `define ADR_A           3'b010

`endif
