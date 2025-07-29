<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## Foreword
The 6502 resources we found compiled online did not reflect the hardware as much as expected
most likely due to the fact that the provided information was for developers using the 6502 and
not the actual design manual itself. 

We also found that the 6502 was made with some strange practices in mind - at the time, microprocessor design 
space was not as advanced and explored; for instance, modern CPUs do not use multi-phase clock signals.

Thus, we decided to make some educated guesses and edits to 'improve' the design for our use cases, and make things easier.
Finally, our code freeze occured before we could add any ADDR X type instructions (incrementing for arrays), 
which were deemed non-essential as they could be implemented via software(through program editing).

Overall though, we do intend for our 6502 to remain relatively authentic.

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

In the descriptions below, a "CPU Cycle" refers to a complete state transition in the processor's core logic. Due to the I/O multiplexing scheme, each CPU Cycle takes two cycles of the main input `clk`. 

---

#### 1. Implied and Register Addressing

These are the simplest modes. The instruction operates directly on a register or has no operand, so the instruction itself is a single byte.

*   **Example:** `TAX` (Transfer Accumulator to X Register)
*   **Instruction Format:** `8A`
*   **CPU Cycles:** 2
*   **Cycle-by-Cycle Breakdown:**
    *   **Cycle 1 (Fetch Opcode):** The PC is placed onto the address bus, and `8A` is read. The PC is incremented.
    *   **Cycle 2 (Execute):** The value in the Accumulator is placed into X using `bus1` as the intermediary

---

#### 2. Accumulator Addressing

In this mode, the instruction operates directly on the Accumulator. Like Implied addressing, it is a single-byte instruction. It is primarily used for shift and rotate operations.

*   **Example:** `ASL A` (Arithmetic Shift Left on Accumulator)
*   **Instruction Format:** `0A`
*   **CPU Cycles:** 4
*   **Cycle-by-Cycle Breakdown:**
    *   **Cycle 1 (Fetch Opcode):** The PC is placed onto the address bus, and `0A` is read. The PC is incremented.
    *   **Cycle 2 (Execute):** The value in the accumulator is sent to the ALU, which is given the `ASL` Opcode and performs the Left Shift operation. The result is calculated and flags are updated.
    *   **Cycle 3 (Transfer Result):** The output from the ALU is written to `bus2` and the Accumulator is told to read from `bus2`
    *   **Cycle 4 (Hold):** The accumulator reads from `bus2` with the final value

---

#### 3. Immediate Addressing

The operand for the instruction is the literal value contained in the byte immediately following the opcode.

*   **Example (Load):** `LDA #44` (Load Accumulator with the value `$44`)
*   **Instruction Format:** `A9 44`
*   **CPU Cycles:** 5
*   **Cycle-by-Cycle Breakdown:**
    *   **Cycle 1 (Fetch Opcode):** The PC is placed onto the address bus, and `A9` is read. The PC is incremented.
    *   **Cycle 2 (Read from Memory):** The PC is placed on the address bus. The data at that location is read into the `Input Data Latch`. The PC is Incremented
    *   **Cycle 3 (Transfer Result):** The data from the latch is written to `bus1` and the Accumulator is told to read from `bus1`
    *   **Cycle 4 (Hold):** The accumulator reads from `bus1` with the final value
    *   **Cycle 5 (None):** The cpu does nothing here due to the fixed machine state path

*   **Example (Read-Modify-Write to Accumulator):** `ORA #44` (OR Accumulator with the value `$44`)
*   **Instruction Format:** `09 44`
*   **CPU Cycles:** 5
*   **Cycle-by-Cycle Breakdown:**
    *   **Cycle 1 (Fetch Opcode):** The PC is placed onto the address bus, and `09` is read. The PC is incremented.
    *   **Cycle 2 (Read from Memory):** The PC is placed on the address bus. The data at that location is read into the `Input Data Latch`. The PC is Incremented
    *   **Cycle 3 (Execute):** The data from the latch and the value in the Accumulator is sent to the ALU, which is given the `AND` Opcode and performs the Left Shift operation. The result is calculated and flags are updated.
    *   **Cycle 3 (Transfer Result):** The output from the ALU is written to `bus2` and the Accumulator is told to read from `bus2`
    *   **Cycle 4 (Hold):** The accumulator reads from `bus2` with the final value
---

#### 4. Zero-Page Addressing

This mode provides faster memory access by using a single byte to specify an address within the first 256 bytes of memory (Page 0, addresses `$0000` to `$00FF`).

*   **Example (Load):** `LDA $44` (Load Accumulator from address `$0044`)
*   **Instruction Format:** `A5 44`
*   **CPU Cycles:** 4
*   **Cycle-by-Cycle Breakdown:**
    *   **Cycle 1 (Fetch Opcode):** Fetches the opcode (`$A5`). PC is incremented.
    *   **Cycle 2 (Fetch ZP Address):** Fetches the operand (`$44`), which is the low byte of the effective address. PC is incremented.
    *   **Cycle 3 (Read from Memory):** The full address (`$0044`) is placed on the address bus. The data at that location is read into the `Input Data Latch`.
    *   **Cycle 4 (Writeback):** The value is loaded from the Input Data Latch into the Accumulator.

*   **Example (Read-Modify-Write To Accumulator):** `AND $44` (AND the Accumulator and the byte at address `$0044` and write to the Accumulator)
*   **Instruction Format:** `25 44`
*   **CPU Cycles:** 6
*   **Cycle-by-Cycle Breakdown:**
    *   **Cycle 1 (Fetch Opcode):** The PC is placed onto the address bus, and `25` is read. The PC is incremented.
    *   **Cycle 2 (Fetch ZP Address):** Fetches the operand (`$44`), which is the low byte of the effective address. PC is incremented.
    *   **Cycle 3 (Read from Memory):** The full address (`$0044`) is placed on the address bus. The data at that location is read into the `Input Data Latch`.
    *   **Cycle 4 (Execute):** The data from the latch and the value in the Accumulator is sent to the ALU, which is given the `AND` Opcode and performs the Left Shift operation. The result is calculated and flags are updated.
    *   **Cycle 5 (Transfer Result):** The output from the ALU is written to `bus2` and the Accumulator is told to read from `bus2`
    *   **Cycle 6 (Hold):** The accumulator reads from `bus2` with the final value

*   **Example (Read-Modify-Write To Memory):** `ASL $44` (Arithmetic Shift Left on the byte at address `$0044`)
*   **Instruction Format:** `06 44`
*   **CPU Cycles:** 7
*   **Cycle-by-Cycle Breakdown:**
    *   **Cycle 1 (Fetch Opcode):** The PC is placed onto the address bus, and `0A` is read. The PC is incremented.
    *   **Cycle 2 (Fetch ZP Address):** Fetches the operand (`$44`), which is the low byte of the effective address. PC is incremented.
    *   **Cycle 3 (Read from Memory):** The full address (`$0044`) is placed on the address bus. The data at that location is read into the `Input Data Latch`.
    *   **Cycle 4 (Execute):** The data from the latch is sent to the ALU, which is given the `ASL` Opcode and performs the Left Shift operation. The result is calculated and flags are updated.
    *   **Cycle 5 (Transfer to Buffer):** The output value from the ALU is loaded into the `Data Bus Buffer` 
    *   **Cycle 6 (Writeback to Memory):** The HB of the address (`$00`) is placed on the address bus, and the `Data Bus Buffer` content is written to the IO Bus.
    *   **Cycle 7 (Write Address LB to address bus):** The LB of the address (`$44`) is placed on the address bus, and the IO Bus content is written to memory(this step is mostly off chip)
---

#### 5. Absolute Addressing

This mode uses a full 16-bit address to access any location in the 64KB memory space. The address follows the opcode as two bytes in little-endian format (low byte first).

*   **Example (Read-Modify-Write To Accumulator):** `EOR $1234` (XOR the Accumulator and the byte at address `$1234` and write to the Accumulator)
*   **Instruction Format:** `4d 44`
*   **CPU Cycles:** 7
*   **Cycle-by-Cycle Breakdown:**
    *   **Cycle 1 (Fetch Opcode):** The PC is placed onto the address bus, and `25` is read. The PC is incremented.
    *   **Cycle 2 (Fetch Address Low Byte):** Fetches the low byte of the address (`$34`) and writes it to an internal buffer. PC is incremented.
    *   **Cycle 3 (Fetch Address High Byte):** Fetches the high byte of the address (`$12`). The full address `$1234` is now assembled. PC is incremented.
    *   **Cycle 3 (Read from Memory):** The full address (`$0044`) is placed on the address bus. The data at that location is read into the `Input Data Latch`.
    *   **Cycle 4 (Execute):** The data from the latch and the value in the Accumulator is sent to the ALU, which is given the `AND` Opcode and performs the Left Shift operation. The result is calculated and flags are updated.
    *   **Cycle 5 (Transfer Result):** The output from the ALU is written to `bus2` and the Accumulator is told to read from `bus2`
    *   **Cycle 6 (Hold):** The accumulator reads from `bus2` with the final value

*   **Example (Read-Write-Modify to Memory):** `STA $1234` (Store Accumulator at address `$1234`)
*   **Instruction Format:** `8D 34 12`
*   **CPU Cycles:** 8
*   **Cycle-by-Cycle Breakdown:**
    *   **Cycle 1 (Fetch Opcode):** The PC is placed onto the address bus, and `8D` is read. The PC is incremented.
    *   **Cycle 2 (Fetch Address Low Byte):** Fetches the low byte of the address (`$34`) and writes it to an internal buffer. PC is incremented.
    *   **Cycle 3 (Fetch Address High Byte):** Fetches the high byte of the address (`$12`). The full address `$1234` is now assembled. PC is incremented.
    *   **Cycle 4 (Read from Memory):** The hardware reads from the target address (`$1234`). For a store instruction, this read is superfluous but occurs due to the fixed state machine path.
    *   **Cycle 5 (Execute):** The ALU performs no meaningful operation for a store instruction.
    *   **Cycle 6 (Transfer to Buffer):** The value in the Accumulator is placed on `bus2` and loaded into the `Data Bus Buffer`.
    *   **Cycle 7 (Writeback to Memory):** The HB of the address (`$12`) is placed on the address bus, and the `Data Bus Buffer` content is written to the IO Bus.
    *   **Cycle 8 (Write Address LB to address bus):** The LB of the address (`$34`) is placed on the address bus, and the IO Bus content is written to memory(this step is mostly off chip)


## How to test

run a fake memory maybe????

## Errata

Table of Supported Instructions:

|Instruction Name                   | Instruction Format | Time Taken      | Flags Changed |
|-----------------------------------|--------------------|-----------------|---------------|
|ARITHMETIC ZPG INSTRUCTIONS                                                               |
|-----------------------------------|--------------------|-----------------|---------------|
|ASL ZPG (Arithmatic Shift Left)    | 06 addr-lb         | 7               |  N Z C - - -  |
|LSR ZPG (Logical Shift Right)      | 46 addr-lb         | 7               |  0 Z C - - -  |
|ROL ZPG (Roll Byte Left)           | 26 addr-lb         | 7               |  N Z C - - -  |
|ROR ZPG (Roll Byte Right)          | 46 addr-lb         | 7               |  N Z C - - -  |
|INC ZPG (Increment Byte)           | c6 addr-lb         | 7               |  N Z - - - -  |
|DEC ZPG (Decrement Byte)           | e6 addr-lb         | 7               |  N Z - - - -  |
|AND ZPG (AND Byte with Acc)        | 35 addr-lb         | 6               |  N Z - - - -  |
|ORA ZPG (OR Byte with Acc)         | 05 addr-lb         | 6               |  N Z - - - -  |
|EOR ZPG (XOR Byte with Acc)        | 55 addr-lb         | 6               |  N Z - - - -  |
|ADC ZPG (Add Byte with Acc)        | 65 addr-lb         | 6               |  N Z C - - V  |
|SBC ZPG (Subtract Byte with Acc)   | e5 addr-lb         | 6               |  N Z C - - V  |
|-----------------------------------|--------------------|-----------------|---------------|
|STORE ZPG INSTRUCTIONS                                                                    |
|-----------------------------------|--------------------|-----------------|---------------|
|STY ZPG (Store Y)                  | 84 addr-lb         | 7               |  - - - - - -  |
|STA ZPG (Store Accumulator)        | 85 addr-lb         | 7               |  - - - - - -  |
|STX ZPG (Store X)                  | 86 addr-lb         | 7               |  - - - - - -  |
|-----------------------------------|--------------------|-----------------|---------------|
|LOAD ZPG INSTRUCTIONS                                                                     |
|-----------------------------------|--------------------|-----------------|---------------|
|LDY ZPG (Load Y)                   | a4 addr-lb         | 6               |  - - - - - -  |
|LDA ZPG (Load Accumulator)         | a5 addr-lb         | 6               |  - - - - - -  |
|LDX ZPG (Load X)                   | a6 addr-lb         | 6               |  - - - - - -  |
|-----------------------------------|--------------------|-----------------|---------------|
|TRANSFER INSTRUCTIONS                                                                     |
|-----------------------------------|--------------------|-----------------|---------------|
|TXA (Transfer from X to Acc)       | 8a                 | 2               |  - - - - - -  |
|TYA (Transfer from Y to Acc)       | 98                 | 2               |  - - - - - -  |
|TAX (Transfer from Acc to X)       | aa                 | 2               |  - - - - - -  |
|TAY (Transfer from Acc to Y)       | a8                 | 2               |  - - - - - -  |
|-----------------------------------|--------------------|-----------------|---------------|
|ARITHMETIC ABS INSTRUCTIONS                                                               |
|-----------------------------------|--------------------|-----------------|---------------|
|ASL ABS (Arithmatic Shift Left)    | 0e addr-lb addr-hb | 8               |  N Z C - - -  |
|LSR ABS (Logical Shift Right)      | 4e addr-lb addr-hb | 8               |  0 Z C - - -  |
|ROL ABS (Roll Byte Left)           | 2e addr-lb addr-hb | 8               |  N Z C - - -  |
|ROR ABS (Roll Byte Right)          | 4e addr-lb addr-hb | 8               |  N Z C - - -  |
|INC ABS (Increment Byte)           | ce addr-lb addr-hb | 8               |  N Z - - - -  |
|DEC ABS (Decrement Byte)           | ee addr-lb addr-hb | 8               |  N Z - - - -  |
|AND ABS (AND Byte with Acc)        | 3d addr-lb addr-hb | 7               |  N Z - - - -  |
|ORA ABS (OR Byte with Acc)         | 0d addr-lb addr-hb | 7               |  N Z - - - -  |
|EOR ABS (XOR Byte with Acc)        | 5d addr-lb addr-hb | 7               |  N Z - - - -  |
|ADC ABS (Add Byte with Acc)        | 6d addr-lb addr-hb | 7               |  N Z C - - V  |
|SBC ABS (Subtract Byte with Acc)   | ed addr-lb addr-hb | 7               |  N Z C - - V  |
|-----------------------------------|--------------------|-----------------|---------------|
|STORE ABS INSTRUCTIONS                                                                    |
|-----------------------------------|--------------------|-----------------|---------------|
|STY ABS (Store Y)                  | 8c addr-lb addr-hb | 8               |  - - - - - -  |
|STA ABS (Store Accumulator)        | 8d addr-lb addr-hb | 8               |  - - - - - -  |
|STX ABS (Store X)                  | 8e addr-lb addr-hb | 8               |  - - - - - -  |
|-----------------------------------|--------------------|-----------------|---------------|
|LOAD ABS INSTRUCTIONS                                                                     |
|-----------------------------------|--------------------|-----------------|---------------|
|LDY ABS (Load Y)                   | ac addr-lb addr-hb | 7               |  - - - - - -  |
|LDA ABS (Load Accumulator)         | ad addr-lb addr-hb | 7               |  - - - - - -  |
|LDX ABS (Load X)                   | ae addr-lb addr-hb | 7               |  - - - - - -  |
|-----------------------------------|--------------------|-----------------|---------------|
|ARITHMETIC IMM INSTRUCTIONS                                                               |
|-----------------------------------|--------------------|-----------------|---------------|
|ASL IMM (Arithmatic Shift Left)    | 09 imm             | 5               |  N Z C - - -  |
|LSR IMM (Logical Shift Right)      | 49 imm             | 5               |  0 Z C - - -  |
|ROL IMM (Roll Byte Left)           | 29 imm             | 5               |  N Z C - - -  |
|ROR IMM (Roll Byte Right)          | 49 imm             | 5               |  N Z C - - -  |
|-----------------------------------|--------------------|-----------------|---------------|
|INC/DEC REGISTER INSTRUCTIONS                                                             |
|-----------------------------------|--------------------|-----------------|---------------|
|INX (Increment X)                  | e8                 | 4               |  - - - - - -  |
|INY (Increment Y)                  | c8                 | 4               |  - - - - - -  |
|DEX (Decrement X)                  | ca                 | 4               |  - - - - - -  |
|DEY (Decrement Y)                  | 88                 | 4               |  - - - - - -  |
|-----------------------------------|--------------------|-----------------|---------------|
|ARITHMETIC ACC INSTRUCTIONS                                                               |
|-----------------------------------|--------------------|-----------------|---------------|
|ASL A (Arithmatic Shift Left Acc)  | 0a                 | 4               |  N Z C - - -  |
|LSR A (Logical Shift Right Acc)    | 4a                 | 4               |  N Z C - - -  |
|ROL A (Roll Byte Left Acc)         | 2a                 | 4               |  N Z C - - -  |
|ROR A (Roll Byte Right Acc)        | 6a                 | 4               |  N Z C - - -  |
|SBC A (Subtract Byte with Acc)     | ea                 | 4               |  N Z C - - V  |
|-----------------------------------|--------------------|-----------------|---------------|
|OTHER INSTRUCTIONS                                                                        |
|-----------------------------------|--------------------|-----------------|---------------|
|NOP (No Op)                        | ea                 | 2               |  - - - - - -  |
|JMP ABS (Jump)                     | 4c addr-lb addr-hb | 4               |  - - - - - -  |





