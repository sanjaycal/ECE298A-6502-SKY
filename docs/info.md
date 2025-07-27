<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This is a 6502 that has a cpu clock frequency of half the input clock due to IO restrictions

## How to test

run a fake memory maybe????

## External hardware

laptop maybe, not done yet

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



