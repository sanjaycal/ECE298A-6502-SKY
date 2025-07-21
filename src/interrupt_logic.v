`default_nettype none

module interrupt_logic (
    input  wire       clk,
    input  wire       res_in,
    input  wire       irq_in,
    input  wire       nmi_in,
    output  wire       res_out,
    output  wire       irq_out,
    output  wire       nmi_out
);
    assign res_out = res_in;
    assign irq_out = irq_in;
    assign nmi_out = nmi_in;

    wire _unused = &{clk};

endmodule
