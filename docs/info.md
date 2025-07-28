<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works
This project implements a custom 8-bit microprocessor inspired by the 6502 architecture. The design is built around a central Arithmetic Logic Unit (ALU), a collection of registers, and a microcoded instruction decoder that executes a subset of the 6502 instruction set.

### Overview

#### Core Architecture

The processor's operation is coordinated by several key functional blocks:

*   **Instruction Decode:** This is the control center of the CPU. It's a complex finite state machine that reads an instruction from the data bus, interprets its opcode and addressing mode, and generates the internal control signals required to execute it over a series of clock cycles.
*   **Registers:**
    *   **Program Counter (PC):** A 16-bit register that holds the memory address of the next instruction to be fetched.
    *   **Accumulator (A):** An 8-bit register used for most arithmetic and logical operations.
    *   **Index Registers (X and Y):** Two 8-bit registers commonly used for indexed addressing modes and as general-purpose counters or temporary storage.
    *   **Processor Status Register (P):** Contains a set of flags (e.g., Carry, Zero, Negative) that reflect the result of the most recent ALU operation.
*   **Arithmetic Logic Unit (ALU):** The computational core of the processor. It performs all arithmetic (add, increment, decrement) and logical (AND, OR, XOR, shift, rotate) operations. It takes inputs from the internal buses and updates the Processor Status Register flags based on the outcome of its calculation.
*   **Internal Buses (Bus 1 & Bus 2):** Two internal 8-bit buses that serve as the data highways connecting the registers and ALU, allowing for the transfer of operands and results within the CPU.
*   **I/O Buffers:**
    *   **Address Bus (AB):** An internal 16-bit bus that holds the address for memory operations. Its value is selected from either the PC, a calculated memory address, or the ALU output.
    *   **Input Data Latch:** Temporarily holds data read from the main data bus, typically an instruction operand or address byte.
    *   **Data Bus Buffer:** Temporarily holds data from an internal register before it is written out to the main data bus.

#### Operational Cycle

The processor operates on a classic **Fetch-Decode-Execute** cycle controlled by the instruction decoder's state machine:

1.  **Fetch:** The address in the Program Counter (PC) is placed on the Address Bus to read the next instruction byte from memory. This byte is loaded into the instruction decoder. The PC is then incremented.
2.  **Decode:** The decoder logic analyzes the instruction. Based on the opcode, it determines which operation to perform and which addressing mode to use (e.g., Zero Page, Absolute, Immediate). This determines the subsequent states the machine will enter.
3.  **Execute:** The decoder sequences through one or more states to complete the instruction. This multi-cycle process may involve:
    *   Fetching additional bytes from memory for operands or addresses.
    *   Loading data from registers onto the internal buses to be used as ALU inputs.
    *   Triggering an ALU operation.
    *   Capturing the ALU output and flags.
    *   Storing the result back into a register (A, X, or Y) or writing it to a memory location.

#### Clocking and I/O

A unique characteristic of this design is its clocking scheme. The internal CPU logic runs at **half the frequency of the external `clk` input**.

This is a deliberate design choice to manage the physical pin limitations of the hardware.

*   **Address Bus:** The 16-bit address bus (`ab`) is too wide for the available output pins. It is therefore multiplexed and output via the 8-bit `uo_out` port over two consecutive clock cycles.
*   **Data Bus:** The 8-bit bidirectional data bus is handled by the `uio_in`, `uio_out`, and `uio_oe` pins, with the `rw` signal controlling the direction of data flow.

![block diagram](6502BlockDiagram.png)

### Addressing Modes

The processor supports a variety of addressing modes to provide flexibility in accessing data. The specific mode for an instruction is implicitly defined by its opcode.

In the descriptions below, a "CPU Cycle" refers to a complete state transition in the processor's core logic. Due to the I/O multiplexing scheme, each CPU Cycle takes two ticks of the main input `clk`. The cycle-by-cycle analysis is derived directly from the state machine in the `instruction_decode.v` module.

---

#### 1. Implied and Register Addressing

These are the simplest modes. The instruction operates directly on a register or has no operand, so the instruction itself is a single byte.

*   **Example:** `TAX` (Transfer Accumulator to X Register)
*   **Instruction Format:** `8A`
*   **CPU Cycles:** 2
*   **Cycle-by-Cycle Breakdown:**
    *   **Cycle 1 (Fetch Opcode):** The Program Counter (PC) is placed on the address bus. The opcode (`$8A`) is read from the data bus into the instruction register. The PC is incremented.
    *   **Cycle 2 (Execute):** The instruction decoder asserts control lines to place the value of the Accumulator onto internal `Bus 1`. Simultaneously, it enables the Index Register X to load its new value from `Bus 1`, completing the transfer.

---

#### 2. Accumulator Addressing

In this mode, the instruction operates directly on the Accumulator. Like Implied addressing, it is a single-byte instruction. It is primarily used for shift and rotate operations.

*   **Example:** `ASL A` (Arithmetic Shift Left on Accumulator)
*   **Instruction Format:** `0A`
*   **CPU Cycles:** 4
*   **Cycle-by-Cycle Breakdown:**
    *   **Cycle 1 (Fetch Opcode):** The PC is placed on the address bus to fetch the opcode (`$0A`). The PC is incremented.
    *   **Cycle 2 (Execute):** The decoder places the Accumulator's value onto internal `Bus 1`, which is routed to the ALU's Input A. The ALU is commanded to perform the `ASL` operation. The result is calculated and status flags (N, Z, C) are updated.
    *   **Cycle 3 (Transfer Result):** The ALU output containing the shifted value is placed on internal `Bus 2`.
    *   **Cycle 4 (Writeback):** The decoder enables the Accumulator to load the new value from `Bus 2`.

---

#### 3. Immediate Addressing

The operand for the instruction is the literal value contained in the byte immediately following the opcode.

*   **Example:** `LDA #$44` (Load Accumulator with the value `$44`)
*   **Instruction Format:** `A9 44`
*   **CPU Cycles:** 5
*   **Cycle-by-Cycle Breakdown:**
    *   **Cycle 1 (Fetch Opcode):** The opcode (`$A9`) is fetched from the address pointed to by the PC. The PC is incremented.
    *   **Cycle 2 (Fetch Operand):** The PC is placed on the address bus again to fetch the operand (`$44`). The value is read into the `Input Data Latch`. The PC is incremented.
    *   **Cycle 3 (Prep Load):** The value from the `Input Data Latch` is placed on `Bus 1` and passed through the ALU (using the `FLG` op) to set the Negative (N) and Zero (Z) flags.
    *   **Cycle 4 (Transfer Result):** The ALU output is placed on `Bus 2`.
    *   **Cycle 5 (Writeback):** The Accumulator is enabled to load the value from `Bus 2`.

---

#### 4. Zero-Page Addressing

This mode provides faster memory access by using a single byte to specify an address within the first 256 bytes of memory (Page 0, addresses `$0000` to `$00FF`).

*   **Example (Load):** `LDA $44` (Load Accumulator from address `$0044`)
*   **Instruction Format:** `A5 44`
*   **CPU Cycles:** 5
*   **Cycle-by-Cycle Breakdown:**
    *   **Cycle 1 (Fetch Opcode):** Fetches the opcode (`$A5`). PC is incremented.
    *   **Cycle 2 (Fetch ZP Address):** Fetches the operand (`$44`), which is the low byte of the effective address. PC is incremented.
    *   **Cycle 3 (Read from Memory):** The full address (`$0044`) is placed on the address bus. The data at that location is read into the `Input Data Latch`.
    *   **Cycle 4 (Prep Load):** The value from the `Input Data Latch` is passed through the ALU to set the N and Z flags.
    *   **Cycle 5 (Writeback):** The value is loaded from the internal bus into the Accumulator.

*   **Example (Read-Modify-Write):** `ASL $44` (Arithmetic Shift Left on the byte at address `$0044`)
*   **Instruction Format:** `06 44`
*   **CPU Cycles:** 6
*   **Cycle-by-Cycle Breakdown:**
    *   **Cycles 1-3:** Same as `LDA $44` (Fetch Opcode, Fetch ZP Address, Read Data into `Input Data Latch`).
    *   **Cycle 4 (Execute):** The data from the latch is sent to the ALU, which performs the `ASL` operation. The result is calculated and flags are updated.
    *   **Cycle 5 (Transfer to Buffer):** The modified value from the ALU output is loaded into the `Data Bus Buffer` in preparation for writing.
    *   **Cycle 6 (Writeback to Memory):** The address (`$0044`) is placed on the address bus, and the `Data Bus Buffer` content is written to memory.

---

#### 5. Absolute Addressing

This mode uses a full 16-bit address to access any location in the 64KB memory space. The address follows the opcode as two bytes in little-endian format (low byte first).

*   **Example (Store):** `STA $1234` (Store Accumulator at address `$1234`)
*   **Instruction Format:** `8D 34 12`
*   **CPU Cycles:** 7
*   **Cycle-by-Cycle Breakdown:**
    *   **Cycle 1 (Fetch Opcode):** Fetches the opcode (`$8D`). PC is incremented.
    *   **Cycle 2 (Fetch Address Low Byte):** Fetches the low byte of the address (`$34`). PC is incremented.
    *   **Cycle 3 (Fetch Address High Byte):** Fetches the high byte of the address (`$12`). The full address `$1234` is now assembled. PC is incremented.
    *   **Cycle 4 (Read from Memory):** The hardware reads from the target address (`$1234`). For a store instruction, this read is superfluous but occurs due to the fixed state machine path.
    *   **Cycle 5 (ALU Idle):** The ALU performs no meaningful operation for a store instruction.
    *   **Cycle 6 (Transfer to Buffer):** The value in the Accumulator is placed on an internal bus and loaded into the `Data Bus Buffer`.
    *   **Cycle 7 (Writeback to Memory):** The address (`$1234`) is placed on the address bus, and the value from the `Data Bus Buffer` is written to memory.


## How to test

run a fake memory maybe????

## Errata

Table of Supported Instructions:

|Instruction Name                   | Instruction Format | Time Taken      | Flags Changed |
|-----------------------------------|--------------------|-----------------|---------------|
|ARITHMETIC ZPG INSTRUCTIONS        |                    |                 |               |
|-----------------------------------|--------------------|-----------------|---------------|
|ASL ZPG (Arithmatic Shift Left)    | 06 addr-lb         | 7               |  N Z C - - -  |
|LSR ZPG (Logical Shift Right)      | 46 addr-lb         | 7               |  0 Z C - - -  |
|ROL ZPG (Roll Byte Left)           | 26 addr-lb         | 7               |  N Z C - - -  |
|ROR ZPG (Roll Byte Right)          | 46 addr-lb         | 7               |  N Z C - - -  |
|INC ZPG (Increment Byte)           | c6 addr-lb         | 7               |  N Z - - - -  |
|DEC ZPG (Decrement Byte)           | e6 addr-lb         | 7               |  N Z - - - -  |
|AND ZPG (AND Byte with Accumulator)| 35 addr-lb         | 6               |  N Z - - - -  |
|ORA ZPG (OR Byte with Accumulator) | 05 addr-lb         | 6               |  N Z - - - -  |
|EOR ZPG (XOR Byte with Accumulator)| 55 addr-lb         | 6               |  N Z - - - -  |
|-----------------------------------|--------------------|-----------------|---------------|
|STORE ZPG INSTRUCTIONS             |                    |                 |               |
|-----------------------------------|--------------------|-----------------|---------------|
|STY ZPG (Store Y)                  | 84 addr-lb         | 7               |  - - - - - -  |
|STA ZPG (Store Accumulator)        | 85 addr-lb         | 7               |  - - - - - -  |
|STX ZPG (Store X)                  | 86 addr-lb         | 7               |  - - - - - -  |
|-----------------------------------|--------------------|-----------------|---------------|
|LOAD ZPG INSTRUCTIONS              |                    |                 |               |
|-----------------------------------|--------------------|-----------------|---------------|
|LDY ZPG (Load Y)                   | a4 addr-lb         | 6               |  - - - - - -  |
|LDA ZPG (Load Accumulator)         | a5 addr-lb         | 6               |  - - - - - -  |
|LDX ZPG (Load X)                   | a6 addr-lb         | 6               |  - - - - - -  |
|-----------------------------------|--------------------|-----------------|---------------|
|TRANSFER INSTRUCTIONS              |                    |                 |               |
|-----------------------------------|--------------------|-----------------|---------------|
|TXA (Transfer from X to Acc)       | 8a addr-lb         | 2               |  - - - - - -  |
|TYA (Transfer from Y to Acc)       | 98 addr-lb         | 2               |  - - - - - -  |
|TAX (Transfer from Acc to X)       | aa addr-lb         | 2               |  - - - - - -  |
|TAY (Transfer from Acc to Y)       | a8 addr-lb         | 2               |  - - - - - -  |
|-----------------------------------|--------------------|-----------------|---------------|
|INC/DEC REGISTER INSTRUCTIONS      |                    |                 |               |
|-----------------------------------|--------------------|-----------------|---------------|
|INX (Increment X)                  | e8 addr-lb         | 4               |  - - - - - -  |
|INY (Increment Y)                  | c8 addr-lb         | 4               |  - - - - - -  |
|DEX (Decrement X)                  | ca addr-lb         | 4               |  - - - - - -  |
|DEY (Decrement Y)                  | 88 addr-lb         | 4               |  - - - - - -  |
|-----------------------------------|--------------------|-----------------|---------------|
|ARITHMETIC ACCUMULATOR INSTRUCTIONS|                    |                 |               |
|-----------------------------------|--------------------|-----------------|---------------|
|ASL A (Arithmatic Shift Left Acc)  | 0a                 | 4               |  N Z C - - -  |
|LSR A (Logical Shift Right Acc)    | 4a                 | 4               |  N Z C - - -  |
|ROL A (Roll Byte Left Acc)         | 2a                 | 4               |  N Z C - - -  |
|ROR A (Roll Byte Right Acc)        | 6a                 | 4               |  N Z C - - -  |
|-----------------------------------|--------------------|-----------------|---------------|
|OTHER INSTRUCTIONS                 |                    |                 |               |
|-----------------------------------|--------------------|-----------------|---------------|
|NOP (No Op)                        | ea                 | 2               |  - - - - - -  |





