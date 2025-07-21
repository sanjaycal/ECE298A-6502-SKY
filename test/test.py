# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
import random

import helper


@cocotb.test()
async def test_ASL_ZPG_Clear(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(256):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)

        cval = test_num
        pc = 1

        for _ in range(8):
            await helper.test_zpg_instruction(
                dut,
                helper.hex_to_num("06"),
                memory_addr_with_value,
                pc,
                cval,
                (cval * 2) % 256,
            )
            cval = (cval * 2) % 256
            pc += 2

        assert cval == 0


@cocotb.test()
async def test_ASL_ZPG_Base(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(256):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("06"),
            memory_addr_with_value,
            1,
            test_num,
            (test_num * 2) % 256,
        )


@cocotb.test()
async def test_LSR_ZPG_Clear(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(256):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)

        cval = test_num
        pc = 1

        for _ in range(8):
            await helper.test_zpg_instruction(
                dut,
                helper.hex_to_num("46"),
                memory_addr_with_value,
                pc,
                cval,
                (cval // 2) % 256,
            )
            cval = (cval // 2) % 256
            pc += 2

        assert cval == 0


@cocotb.test()
async def test_LSR_ZPG_Base(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("46"),
            memory_addr_with_value,
            1,
            test_num,
            (test_num // 2),
        )


@cocotb.test()
async def test_ROL_ZPG_Loop(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(256):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)

        cval = test_num
        carry = 0
        pc = 1

        for _ in range(8):
            carry = cval // 128
            ncval = ((cval * 2) % 256) + carry
            await helper.test_zpg_instruction(
                dut,
                helper.hex_to_num("26"),
                memory_addr_with_value,
                pc,
                cval,
                ncval,
            )
            cval = ncval
            pc += 2

        assert cval == test_num


@cocotb.test()
async def test_ROL_ZPG_Base(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("26"),
            memory_addr_with_value,
            1,
            test_num,
            (test_num * 2) % 256 + test_num // 128,
        )


@cocotb.test()
async def test_ROR_ZPG_Loop(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(256):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)

        cval = test_num
        carry = 0
        pc = 1

        for _ in range(8):
            carry = cval % 2
            ncval = ((cval // 2) % 256) + 128 * carry
            await helper.test_zpg_instruction(
                dut,
                helper.hex_to_num("66"),
                memory_addr_with_value,
                pc,
                cval,
                ncval,
            )
            cval = ncval
            pc += 2

        assert cval == test_num


@cocotb.test()
async def test_ROR_ZPG_Base(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("66"),
            memory_addr_with_value,
            1,
            test_num,
            (test_num // 2) % 256 + 128 * (test_num % 2),
        )


@cocotb.test()
async def test_ASL_ABS_Clear(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)

        cval = test_num
        pc = 1

        for _ in range(8):
            await helper.run_abs_instruction(
                dut,
                helper.hex_to_num("0e"),
                memory_addr_with_value_HB,
                memory_addr_with_value_LB,
                pc,
                cval,
                (cval * 2) % 256,
            )
            cval = (cval * 2) % 256
            pc += 3

        assert cval == 0


@cocotb.test()
async def test_ASL_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)
        await helper.run_abs_instruction(
            dut,
            helper.hex_to_num("0e"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            test_num,
            (test_num * 2) % 256,
        )


@cocotb.test()
async def test_LSR_ABS_Clear(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)

        cval = test_num
        pc = 1

        for _ in range(8):
            await helper.run_abs_instruction(
                dut,
                helper.hex_to_num("4e"),
                memory_addr_with_value_HB,
                memory_addr_with_value_LB,
                pc,
                cval,
                (cval // 2) % 256,
            )
            cval = (cval // 2) % 256
            pc += 3

        assert cval == 0


@cocotb.test()
async def test_LSR_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)
        await helper.run_abs_instruction(
            dut,
            helper.hex_to_num("4e"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            test_num,
            (test_num // 2) % 256,
        )


@cocotb.test()
async def test_ROL_ABS_Loop(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)

        cval = test_num
        carry = 0
        pc = 1

        for _ in range(8):
            carry = cval // 128
            ncval = ((cval * 2) % 256) + carry
            await helper.run_abs_instruction(
                dut,
                helper.hex_to_num("2e"),
                memory_addr_with_value_HB,
                memory_addr_with_value_LB,
                pc,
                cval,
                ncval,
            )
            cval = ncval
            pc += 3

        assert cval == test_num


@cocotb.test()
async def test_ROL_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)
        await helper.run_abs_instruction(
            dut,
            helper.hex_to_num("2e"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            test_num,
            (test_num * 2) % 256 + test_num // 128,
        )


@cocotb.test()
async def test_ROR_ABS_Loop(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)

        cval = test_num
        carry = 0
        pc = 1

        for _ in range(8):
            carry = cval % 2
            ncval = ((cval // 2) % 256) + 128 * carry
            await helper.run_abs_instruction(
                dut,
                helper.hex_to_num("6e"),
                memory_addr_with_value_HB,
                memory_addr_with_value_LB,
                pc,
                cval,
                ncval,
            )
            cval = ncval
            pc += 3

        assert cval == test_num


@cocotb.test()
async def test_ROR_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)
        await helper.run_abs_instruction(
            dut,
            helper.hex_to_num("6e"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            test_num,
            (test_num // 2) % 256 + 128 * (test_num % 2),
        )


@cocotb.test()
async def test_LDX_ZPG_Base(dut):
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    for test_num in range(1, 256):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a6"), memory_addr_with_value, 1, test_num
        )
        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("86"), memory_addr_with_value, 3, 0, test_num
        )


@cocotb.test()
async def test_LDA_ZPG_Base(dut):
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    for test_num in range(1, 256):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, test_num
        )
        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("85"), memory_addr_with_value, 3, 0, test_num
        )


@cocotb.test()
async def test_LDY_ZPG_Base(dut):
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    for test_num in range(1, 256):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a3"), memory_addr_with_value, 1, test_num
        )
        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("83"), memory_addr_with_value, 3, 0, test_num
        )


@cocotb.test()
async def test_AND_ZPG_Base(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, acc_value
        )  # LDA
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("25"), memory_addr_with_value, 3, test_num
        )  # AND
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value,
            5,
            0,
            test_num & acc_value,
        )  # STA


@cocotb.test()
async def test_INC_ZPG_Base(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("e6"),
            memory_addr_with_value,
            1,
            test_num,
            (test_num + 1) % 256,
        )  # INC
