/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

 
`include "../inc/alu_ops.vh"
`include "../inc/buf_instructions.vh"


  localparam BUF_IDLE_TWO      = 2'b00;
  localparam BUF_LOAD_TWO      = 2'b01; // Take from a BUS and keep
  localparam BUF_STORE_TWO     = 2'b10; // Put the register value on a BUS
  
  localparam BUF_IDLE_THREE    = 3'b000;
  localparam BUF_LOAD1_THREE   = 3'b100; // Take from a BUS and keep
  localparam BUF_LOAD2_THREE   = 3'b101; // Take from a BUS and keep
  localparam BUF_STORE1_THREE  = 3'b110; // Put the register value on a BUS
  localparam BUF_STORE2_THREE  = 3'b111; // Put the register value on a BUS


`include "../src/clock_generator.v"
`include "../src/instruction_decode.v"
`include "../src/interrupt_logic.v"
`include "../src/alu.v"


`default_nettype none

module tt_um_6502 (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  wire [2:0] index_register_y_enable;
  wire [2:0] index_register_x_enable;
  wire [2:0] stack_pointer_register_enable;
  wire [4:0] ALU_op;
  wire [2:0] accumulator_enable;
  wire pc_enable;
  wire [1:0] input_data_latch_enable;
  wire rdy;
  wire rw;
  wire dbe;
  wire res_in;
  wire irq_in;
  wire nmi_in;
  wire res;
  wire irq;
  wire nmi;
  wire clk_cpu;
  wire clk_output;
  wire [1:0] address_select;
  wire [1:0] data_buffer_enable;
  wire processor_status_register_rw;
  wire [6:0] processor_status_register_read;
  wire [6:0] processor_status_register_write;


  reg [15:0] ab;

  reg [7:0] input_data_latch;
  reg [7:0] bus1;
  reg [7:0] bus2;
  reg [7:0] data_bus_buffer=8'b0;

  reg [15:0] pc;
  wire [15:0] memory_address;
  reg [7:0] accumulator;
  reg [7:0] index_register_x;
  reg [7:0] index_register_y;
  wire [7:0] instruction_register;
  reg [6:0] processor_status_register;

  reg [7:0] next_accumulator;
  reg [7:0] next_index_register_x;
  reg [7:0] next_index_register_y;
  reg [7:0] next_data_bus_buffer;
  reg [6:0] next_processor_status_register;

  wire [7:0] ALU_inputA;
  wire [7:0] ALU_inputB;

  wire [7:0] ALU_output;
  wire [7:0] ALU_flags_output;

  clock_generator clockGenerator(clk, clk_cpu, clk_output);
  instruction_decode instructionDecode(
    .instruction                   (instruction_register),
    .clk                           (clk_cpu),
    .res                           (res),
    .irq                           (irq),
    .nmi                           (nmi),
    .rdy                           (rdy),
    .processor_status_register_read(processor_status_register_read),
    .processor_status_register_write(processor_status_register_write),
    .memory_address                (memory_address),
    .address_select                (address_select),
    .processor_status_register_rw  (processor_status_register_rw),
    .rw                            (rw),
    .data_buffer_enable            (data_buffer_enable),
    .input_data_latch_enable       (input_data_latch_enable), 
    .pc_enable                     (pc_enable),
    .accumulator_enable            (accumulator_enable),
    .alu_enable                    (ALU_op),  
    .stack_pointer_register_enable (stack_pointer_register_enable),
    .index_register_X_enable       (index_register_x_enable),
    .index_register_Y_enable       (index_register_y_enable)
  );
  
  alu ALU(
    .clk               (clk_cpu),
    .alu_op            (ALU_op),
    .inputA            (ALU_inputA),
    .inputB            (ALU_inputB),
    .status_flags_in   (processor_status_register),
    .ALU_output        (ALU_output),
    .ALU_flags_output  (ALU_flags_output)
  );

  interrupt_logic interruptLogic(clk, res_in, irq_in, nmi_in, res, irq, nmi);

  always @(*) begin
    bus1 = 8'h00;
    bus2    = 8'h00;
    next_accumulator = accumulator;
    next_index_register_x = index_register_x;
    next_index_register_y = index_register_y;
    next_data_bus_buffer = data_bus_buffer;
    next_processor_status_register = processor_status_register;
    //putting data on the bus 1
    if(input_data_latch_enable == BUF_STORE_TWO) begin
      bus1 = input_data_latch;
    end else if(accumulator_enable == BUF_STORE1_THREE) begin
      bus1 = accumulator;
    end else if(index_register_x_enable == BUF_STORE1_THREE) begin
      bus1 = index_register_x;
    end else if(index_register_y_enable == BUF_STORE1_THREE) begin
      bus1 = index_register_y;
    end
    //reading data from the bus 1
    if(accumulator_enable == BUF_LOAD1_THREE) begin
       next_accumulator = bus1;
    end
    if(index_register_x_enable == BUF_LOAD1_THREE) begin
      next_index_register_x = bus1;
    end
    if(index_register_y_enable == BUF_LOAD1_THREE) begin
      next_index_register_y = bus1;
    end
    //putting data on the bus 2
    if(ALU_op == `TMX) begin
      bus2 = ALU_output;
    end else if(accumulator_enable == BUF_STORE2_THREE) begin
      bus2 = accumulator;
    end else if(index_register_x_enable == BUF_STORE2_THREE) begin
      bus2 = index_register_x;
    end else if(index_register_y_enable == BUF_STORE2_THREE) begin
      bus2 = index_register_y;
    end
    //reading data from the bus 2
    if(data_buffer_enable == BUF_LOAD_TWO) begin
      next_data_bus_buffer = bus2;
    end
    if(accumulator_enable == BUF_LOAD2_THREE) begin
       next_accumulator = bus2;
    end
    if(index_register_x_enable == BUF_LOAD2_THREE) begin
      next_index_register_x = bus2;
    end
    if(index_register_y_enable == BUF_LOAD2_THREE) begin
      next_index_register_y = bus2;
    end
    //alu stuff
    if(ALU_op != `NOP && ALU_op != `TMX) begin
      next_processor_status_register = ALU_flags_output & processor_status_register_write;
    end
  end

  always @(negedge clk_cpu) begin
    if (rst_n == 0) begin
      pc <= 0;
    end else begin
      if (pc_enable) begin
        pc <= pc+1;
      end
    end
  end

  // assign input_data_latch = (input_data_latch_enable == BUF_LOAD_TWO) ? instruction_register : input_data_latch;
  always @(negedge clk_cpu) begin
    if (rst_n == 0) begin
      accumulator <= 0;
      index_register_x <= 0;
      index_register_y <= 0;
      processor_status_register <= 0;
      input_data_latch <= 8'b0;

    end else begin
    // if(rw == 0 && data_buffer_enable == BUF_STORE_TWO) begin
    //   uio_out <= data_bus_buffer;
    // end
      data_bus_buffer <= next_data_bus_buffer;
      index_register_x <= next_index_register_x;
      index_register_y <= next_index_register_y;
      accumulator <= next_accumulator;
      processor_status_register <= next_processor_status_register;
      if(input_data_latch_enable == 1) begin
        input_data_latch <= uio_in;
      end
    end
  end

  // List all unused inputs to prevent warnings
  assign dbe = 0;
  assign irq_in = 0;
  assign nmi_in = 0;
  assign res_in = 0;
  assign processor_status_register_read = processor_status_register;
  wire _unused = &{ena, 1'b0, ui_in, index_register_y_enable, index_register_x_enable, accumulator_enable, input_data_latch_enable, dbe, accumulator, index_register_x, index_register_y, stack_pointer_register_enable, processor_status_register_rw, processor_status_register_read, processor_status_register_write, clk_output, ALU_flags_output};

  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out = clk_cpu?ab[15:8]:ab[7:0];
  assign uio_out = clk_cpu?(data_buffer_enable == 2'd2 ? data_bus_buffer : 8'b0 ) : {7'b0,rw} ;
  assign uio_oe  = rw?8'h00:8'hff;

assign ALU_inputA = bus1;
assign ALU_inputB = bus2;

// The address bus mux
always @(*) begin
    case (address_select)
        2'b00:   ab = pc;
        2'b01:   ab = memory_address;
        2'b10:   ab = {8'h0, ALU_output};
        default: ab = 16'b0;
    endcase
end
            
  assign instruction_register = uio_in;

  assign rdy = rst_n;



endmodule
