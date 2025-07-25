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
|AND ZPG (AND Byte with Accumulator)| e6 addr-lb         | 7               |  N Z - - - -  | 


