/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`include "../inc/alu_ops.vh"
`include "../inc/buf_instructions.vh"

localparam BUF_LOAD_TWO      = 2'b01;
localparam BUF_STORE_TWO     = 2'b10;
localparam BUF_LOAD1_THREE   = 3'b100;
localparam BUF_LOAD2_THREE   = 3'b101;
localparam BUF_STORE1_THREE  = 3'b110;
localparam BUF_STORE2_THREE  = 3'b111;

`include "../src/instruction_decode.v"
`include "../src/interrupt_logic.v"
`include "../src/alu.v"

`default_nettype none

module tt_um_6502 (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

  // Internal signals
  wire [2:0] index_register_y_enable;
  wire [2:0] index_register_x_enable;
  wire [2:0] stack_pointer_register_enable;
  wire [4:0] ALU_op;
  wire [2:0] accumulator_enable;
  wire pc_enable;
  wire [1:0] input_data_latch_enable;
  wire rdy;
  wire rw;
  wire res;
  wire irq;
  wire nmi;
  wire [1:0] address_select;
  wire [1:0] data_buffer_enable;
  wire processor_status_register_rw;
  wire [6:0] processor_status_register_read;
  wire [6:0] processor_status_register_write;
  wire [15:0] memory_address;
  wire [7:0] ALU_output;
  wire [6:0] ALU_flags_output;

  // Buses
  wire [7:0] bus1;
  wire [7:0] bus2;

  // Internal Registers
  reg [15:0] pc = 16'd0;
  reg [7:0] input_data_latch;
  reg [7:0] data_bus_buffer = 8'd0;
  reg [7:0] accumulator = 8'd0;
  reg [7:0] index_register_x = 8'd0;
  reg [7:0] index_register_y = 8'd0;
  reg [6:0] processor_status_register = 7'd0;

  // Clock Enable for 2-phase logic
  reg clk_enable = 1'b0;
  always @(posedge clk) clk_enable <= ~clk_enable;

  // --- MODULE INSTANTIATIONS ---

  instruction_decode instructionDecode (
      .instruction(uio_in), // instruction is read directly from input
      .clk(clk),
      .clk_enable(clk_enable),
      .res(res), .irq(irq), .nmi(nmi), .rdy(rdy),
      .processor_status_register_read(processor_status_register_read),
      .processor_status_register_write(processor_status_register_write),
      .memory_address(memory_address),
      .address_select(address_select),
      .processor_status_register_rw(processor_status_register_rw),
      .rw(rw),
      .data_buffer_enable(data_buffer_enable),
      .input_data_latch_enable(input_data_latch_enable),
      .pc_enable(pc_enable),
      .accumulator_enable(accumulator_enable),
      .alu_enable(ALU_op),
      .stack_pointer_register_enable(stack_pointer_register_enable),
      .index_register_X_enable(index_register_x_enable),
      .index_register_Y_enable(index_register_y_enable)
  );

  alu ALU (
      .clk(clk),
      .alu_op(ALU_op),
      .inputA(bus1),
      .inputB(bus2),
      .status_flags_in(processor_status_register),
      .ALU_output(ALU_output),
      .ALU_flags_output(ALU_flags_output)
  );

  // Let's assume these are tied off for now
  wire res_in, irq_in, nmi_in;
  interrupt_logic interruptLogic(clk, res_in, irq_in, nmi_in, res, irq, nmi);

  // --- COMBINATIONAL LOGIC ---

  wire [15:0] ab = (address_select == 2'b00) ? pc :
                   (address_select == 2'b01) ? memory_address :
                   (address_select == 2'b10) ? {8'h00, ALU_output} :
                   16'd0;

  assign bus1 = (input_data_latch_enable == BUF_STORE_TWO) ? input_data_latch :
                (accumulator_enable == BUF_STORE1_THREE) ? accumulator :
                (index_register_x_enable == BUF_STORE1_THREE) ? index_register_x :
                (index_register_y_enable == BUF_STORE1_THREE) ? index_register_y :
                8'd0;

  assign bus2 = (ALU_op == `TMX) ? ALU_output :
                (accumulator_enable == BUF_STORE2_THREE) ? accumulator :
                (index_register_x_enable == BUF_STORE2_THREE) ? index_register_x :
                (index_register_y_enable == BUF_STORE2_THREE) ? index_register_y :
                8'd0;

  // --- OUTPUT REGISTERS AND ASSIGNMENTS ---

  reg [7:0] uo_out_reg;
  reg [7:0] uio_out_reg;
  reg [7:0] uio_oe_reg;

  assign uo_out = uo_out_reg;
  assign uio_out = uio_out_reg;
  assign uio_oe = uio_oe_reg;

  // --- MAIN SEQUENTIAL BLOCK ---

  always @(posedge clk) begin
      if (!rst_n) begin
          // Asynchronous reset condition
          pc <= 16'd0;
          accumulator <= 8'd0;
          index_register_x <= 8'd0;
          index_register_y <= 8'd0;
          processor_status_register <= 7'd0;
          input_data_latch <= 8'd0;
          data_bus_buffer <= 8'd0;
          uo_out_reg = 8'd0;
          uio_out_reg <= 8'd0;
          uio_oe_reg <= 8'h00;
      end else begin
          // Default assignments (hold value)
          uo_out_reg = uo_out_reg;
          uio_out_reg <= uio_out_reg;

          // Logic for the "first phase" of the internal clock
          if (clk_enable) begin
              // Update PC
              if (pc_enable) begin
                  pc <= pc + 1;
              end

              // Update main registers from buses
              if (accumulator_enable == BUF_LOAD1_THREE) accumulator <= bus1;
              if (index_register_x_enable == BUF_LOAD1_THREE) index_register_x <= bus1;
              if (index_register_y_enable == BUF_LOAD1_THREE) index_register_y <= bus1;

              if (data_buffer_enable == BUF_LOAD_TWO) data_bus_buffer <= bus2;
              if (accumulator_enable == BUF_LOAD2_THREE) accumulator <= bus2;
              if (index_register_x_enable == BUF_LOAD2_THREE) index_register_x <= bus2;
              if (index_register_y_enable == BUF_LOAD2_THREE) index_register_y <= bus2;

              // Update status register from ALU
              if (ALU_op != `NOP && ALU_op != `TMX) begin
                  processor_status_register <= ALU_flags_output & processor_status_register_write;
              end

              // Update output registers for the first phase
              uo_out_reg = ab[7:0]; // Low byte of address bus
              uio_out_reg <= {7'b0, rw}; // Status
          end
          // Logic for the "second phase" of the internal clock
          else begin // if !clk_enable
              // Latch input data
              if (input_data_latch_enable == 1) begin
                  input_data_latch <= uio_in;
              end

              // Update output registers for the second phase
              uo_out_reg = ab[15:8]; // High byte of address bus
              if (data_buffer_enable == BUF_STORE_TWO) begin
                  uio_out_reg <= data_bus_buffer;
              end
          end

          // Update uio_oe continuously based on rw
          // This can be combinational if rw is stable, but registering is safer
          if (rw) begin
              uio_oe_reg <= 8'h00; // read mode (input)
          end else begin
              uio_oe_reg <= 8'hFF; // write mode (output)
          end
      end
  end

  // --- Unused signals and constants ---
  assign rdy = rst_n;
  assign res_in = ~rst_n;
  assign irq_in = 1'b0;
  assign nmi_in = 1'b0;
  assign processor_status_register_read = processor_status_register;
  wire _unused = &{ena, ui_in, stack_pointer_register_enable};

endmodule
