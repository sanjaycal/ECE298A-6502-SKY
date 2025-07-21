
`default_nettype none

module clock_generator (
    input  wire       clk,
    output  wire       clk_cpu,
    output  wire       clk_output
);
    reg val=0;
    assign clk_cpu = val;
    assign clk_output = clk;
    
    always @(posedge clk) begin
        val <= ~val;
    end
    

endmodule
