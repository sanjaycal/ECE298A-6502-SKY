`ifndef BUF_INSTRUCTIONS
    `define BUF_INSTRUCTIONS 1

    `define BUF_IDLE_TWO      2'b00;
    `define BUF_LOAD_TWO      2'b01; // Take from a BUS and keep
    `define BUF_STORE_TWO     2'b10; // Put the register value on a BUS
    `define BUF_IDLE_THREE    3'b000;
    `define BUF_LOAD1_THREE   3'b100; // Take from a BUS and keep
    `define BUF_LOAD2_THREE   3'b101; // Take from a BUS and keep
    `define BUF_STORE1_THREE  3'b110; // Put the register value on a BUS
    `define BUF_STORE2_THREE  3'b111; // Put the register value on a BUS
`endif
