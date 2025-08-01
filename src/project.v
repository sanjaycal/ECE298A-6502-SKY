/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

 
`include "../inc/alu_ops.vh"
`include "../inc/buf_instructions.vh"


  //localparam BUF_IDLE_TWO      = 2'b00;
  // localparam BUF_LOAD_TWO      = 2'b01; // Take from a BUS and keep
  // localparam BUF_STORE_TWO     = 2'b10; // Put the register value on a BUS
  // localparam PC_INC_ONE        = 3'b111;
  // //localparam BUF_IDLE_THREE    = 3'b000;
  // localparam BUF_LOAD1_THREE   = 3'b100; // Take from a BUS and keep
  // localparam BUF_LOAD2_THREE   = 3'b101; // Take from a BUS and keep
  // localparam BUF_STORE1_THREE  = 3'b110; // Put the register value on a BUS
  // localparam BUF_STORE2_THREE  = 3'b111; // Put the register value on a BUS


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
  wire [2:0] pc_enable;
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
  wire [1:0] address_select;
  wire [1:0] data_buffer_enable;
  wire processor_status_register_rw;
  wire [6:0] processor_status_register_read;
  wire [6:0] processor_status_register_write;
  wire [7:0] processor_status_register_value;


  wire [15:0] ab;

  reg [7:0] input_data_latch = 0;
  wire [7:0] bus1;
  wire [7:0] bus2;
  reg [7:0] data_bus_buffer=8'b0;

  reg [15:0] pc=0;
  wire [15:0] memory_address;
  reg [7:0] accumulator=0;
  reg [7:0] index_register_x=0;
  reg [7:0] index_register_y=0;
  wire [7:0] instruction_register;
  reg [6:0] processor_status_register=0;

  reg [7:0] next_accumulator=0;
  reg [7:0] next_index_register_x=0;
  reg [7:0] next_index_register_y=0;
  reg [7:0] next_data_bus_buffer=0;
  reg [6:0] next_processor_status_register=0;

  wire [7:0] ALU_inputA;
  wire [7:0] ALU_inputB;

  wire [7:0] ALU_output;
  wire [6:0] ALU_flags_output;
  reg clk_enable = 1;

  instruction_decode instructionDecode(
    .instruction                   (instruction_register),
    .clk                           (clk),
    .clk_enable                    (clk_enable),
    .rst_n                         (rst_n),
    .irq                           (irq),
    .nmi                           (nmi),
    .processor_status_register_read(processor_status_register_read),
    .processor_status_register_write(processor_status_register_write),
    .processor_status_register_value(processor_status_register_value),
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
    .clk               (clk),
    .alu_op            (ALU_op),
    .inputA            (ALU_inputA),
    .inputB            (ALU_inputB),
    .status_flags_in   (processor_status_register),
    .ALU_output        (ALU_output),
    .ALU_flags_output  (ALU_flags_output)
  );

  interrupt_logic interruptLogic(clk, res_in, irq_in, nmi_in, res, irq, nmi);

  //putting data on the bus 1
  assign bus1 = (input_data_latch_enable == `BUF_STORE_TWO)?input_data_latch:
                (accumulator_enable == `BUF_STORE1_THREE)?accumulator:
		(index_register_x_enable == `BUF_STORE1_THREE)?index_register_x:
		(index_register_y_enable == `BUF_STORE1_THREE)?index_register_y:
		0;
  //putting data on the bus 2
  assign bus2 = (ALU_op == `TMX)?ALU_output:
                (accumulator_enable == `BUF_STORE2_THREE)?accumulator:
		(index_register_x_enable == `BUF_STORE2_THREE)?index_register_x:
		(index_register_y_enable == `BUF_STORE2_THREE)?index_register_y:
		0;

  always @(posedge clk or negedge rst_n) begin
    if (rst_n == 0) begin
      // Reset all state elements to a known value
      pc <= 16'h0000;
      accumulator <= 8'h00;
      index_register_x <= 8'h00;
      index_register_y <= 8'h00;
      processor_status_register <= 7'h00;
      input_data_latch <= 8'h00;
      data_bus_buffer <= 8'h00;
    next_accumulator <= 0;
    next_index_register_x <= 0;
    next_index_register_y <= 0;
    next_data_bus_buffer <= 0;
    next_processor_status_register <= 0;
    clk_enable <= 1;
    end else begin
    clk_enable <= ~clk_enable;
    next_accumulator <= accumulator;
    next_index_register_x <= index_register_x;
    next_index_register_y <= index_register_y;
    next_data_bus_buffer <= data_bus_buffer;
    //reading data from the bus 1
    if(accumulator_enable == `BUF_LOAD1_THREE) begin
       next_accumulator <= bus1;
    end
    if(index_register_x_enable == `BUF_LOAD1_THREE) begin
      next_index_register_x <= bus1;
    end
    if(index_register_y_enable == `BUF_LOAD1_THREE) begin
      next_index_register_y <= bus1;
    end
    //reading data from the bus 2
    if(data_buffer_enable == `BUF_LOAD_TWO) begin
      next_data_bus_buffer <= bus2;
    end
    if(accumulator_enable == `BUF_LOAD2_THREE) begin
       next_accumulator <= bus2;
    end
    if(index_register_x_enable == `BUF_LOAD2_THREE) begin
      next_index_register_x <= bus2;
    end
    if(index_register_y_enable == `BUF_LOAD2_THREE) begin
      next_index_register_y <= bus2;
    end
    //alu stuff
    if(ALU_op != `NOP && ALU_op == `TMX) begin
      next_processor_status_register <= (ALU_flags_output & processor_status_register_write) | (processor_status_register & ~processor_status_register_write);
    end else if (processor_status_register_value[7]==1) begin
      next_processor_status_register <= (processor_status_register_value[6:0] & processor_status_register_write) | (processor_status_register & ~processor_status_register_write);
    end else begin
      next_processor_status_register <= processor_status_register;
    end
    if(clk_enable==0)begin
      if (rst_n == 0) begin
        processor_status_register <= 0;
        input_data_latch <= 8'b0;
        pc <= 0;

      end else begin
        if(input_data_latch_enable == 1) begin
          input_data_latch <= uio_in;
        end
        if(pc_enable == `PC_INC_ONE) begin
          pc <= pc + 1;
        end
        else if(pc_enable == `BUF_LOAD1_THREE) begin
          pc <= memory_address;
        end
        else if(pc_enable == `PC_TAKE_BRANCH) begin
          pc <= pc + $signed(bus1);
        end
      end
    end else begin
      if (rst_n == 0) begin
        accumulator <= 0;
        data_bus_buffer <= 0;
        index_register_x <= 0;
        index_register_y <= 0;

      end else begin
        processor_status_register <= next_processor_status_register;
        accumulator <= next_accumulator;
        data_bus_buffer <= next_data_bus_buffer;
        index_register_x <= next_index_register_x;
        index_register_y <= next_index_register_y;
      end
    end
  end
  end

  // List all unused inputs to prevent warnings
  assign dbe = 0;
  assign irq_in = 0;
  assign nmi_in = 0;
  assign res_in = 0;
  assign processor_status_register_read = processor_status_register;
  wire _unused = &{ena, 1'b0, dbe, res, rdy, stack_pointer_register_enable, ui_in, processor_status_register_rw};

  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out = (clk_enable==0)?ab[15:8]:ab[7:0];
  assign uio_out = (clk_enable==0)?(data_buffer_enable == 2'd2 ? data_bus_buffer : 8'b0 ) : {7'b0,rw} ;
  assign uio_oe  = rw?8'h00:8'hff;

assign ALU_inputA = bus1;
assign ALU_inputB = bus2;

// The address bus mux
  assign ab = (address_select==2'b00)?pc:
	    	(address_select==2'b01)?memory_address:
		(address_select==2'b10)?{8'h0, ALU_output}:
		0;
            
  assign instruction_register = uio_in;

  assign rdy = rst_n;



endmodule
