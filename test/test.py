# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
import random

import helper

MAX_TESTS = 8  # for the fuzz tests
MAX_TEST_NUM = 255  # for the instruction specific tests


@cocotb.test()
async def test_ASL_ZPG_Clear(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(MAX_TEST_NUM):
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
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(MAX_TEST_NUM):
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
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(MAX_TEST_NUM):
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
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
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
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(MAX_TEST_NUM):
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
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
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
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(MAX_TEST_NUM):
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
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
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
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)

        cval = test_num
        pc = 1

        for _ in range(8):
            await helper.test_abs_instruction(
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
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)
        await helper.test_abs_instruction(
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
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)

        cval = test_num
        pc = 1

        for _ in range(8):
            await helper.test_abs_instruction(
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
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)
        await helper.test_abs_instruction(
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
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)

        cval = test_num
        carry = 0
        pc = 1

        for _ in range(8):
            carry = cval // 128
            ncval = ((cval * 2) % 256) + carry
            await helper.test_abs_instruction(
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
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)
        await helper.test_abs_instruction(
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
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    # test instruction on it's own
    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)

        cval = test_num
        carry = 0
        pc = 1

        for _ in range(8):
            carry = cval % 2
            ncval = ((cval // 2) % 256) + 128 * carry
            await helper.test_abs_instruction(
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
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(1, 255)
        await helper.reset_cpu(dut)
        await helper.test_abs_instruction(
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
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a6"), memory_addr_with_value, 1, test_num
        )
        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("86"), memory_addr_with_value, 3, 0, test_num
        )


@cocotb.test()
async def test_LDX_ABS_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value_HB = random.randint(10, 255)
        memory_addr_with_value_LB = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ae"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            test_num,
        )  # LDX ABS
        await helper.test_abs_instruction(
            dut,
            helper.hex_to_num("8e"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            4,
            0,
            test_num,
        )  # STX ABS


@cocotb.test()
async def test_LDX_IMM_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_for_verify = random.randint(10, 255)

        await helper.reset_cpu(dut)

        await helper.test_imm_instruction(dut, helper.hex_to_num("a2"), 1, test_num)

        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("86"), memory_addr_for_verify, 3, 0, test_num
        )


@cocotb.test()
async def test_LDA_ZPG_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, test_num
        )
        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("85"), memory_addr_with_value, 3, 0, test_num
        )


@cocotb.test()
async def test_LDA_ABS_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)

        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ad"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            test_num,
        )  # LDA ABS
        await helper.test_abs_instruction(
            dut,
            helper.hex_to_num("8d"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            4,
            0,
            test_num,
        )  # STA ABS


@cocotb.test()
async def test_LDA_IMM_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_for_verify = random.randint(10, 255)

        await helper.reset_cpu(dut)

        await helper.test_imm_instruction(dut, helper.hex_to_num("a9"), 1, test_num)

        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("85"), memory_addr_for_verify, 3, 0, test_num
        )


@cocotb.test()
async def test_LDY_ZPG_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a4"), memory_addr_with_value, 1, test_num
        )
        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("84"), memory_addr_with_value, 3, 0, test_num
        )


@cocotb.test()
async def test_LDY_ABS_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, 256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)

        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ac"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            test_num,
        )  # LDY ABS
        await helper.test_abs_instruction(
            dut,
            helper.hex_to_num("8c"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            4,
            0,
            test_num,
        )  # STY ABS


@cocotb.test()
async def test_LDY_IMM_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_for_verify = random.randint(10, 255)

        await helper.reset_cpu(dut)

        await helper.test_imm_instruction(dut, helper.hex_to_num("a0"), 1, test_num)

        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("84"), memory_addr_for_verify, 3, 0, test_num
        )


@cocotb.test()
async def test_AND_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
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
async def test_AND_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ad"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            acc_value,
        )  # LDA
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("2d"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            4,
            test_num,
        )  # AND
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value_LB,
            7,
            0,
            test_num & acc_value,
        )  # STA


@cocotb.test()
async def test_AND_IMM_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ad"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            acc_value,
        )  # LDA
        await helper.run_input_imm_instruction(
            dut,
            helper.hex_to_num("29"),
            4,
            test_num,
        )  # OR Imm
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value_LB,
            6,
            0,
            test_num & acc_value,
        )  # STA


@cocotb.test()
async def test_ORA_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, acc_value
        )  # LDA
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("05"), memory_addr_with_value, 3, test_num
        )  # OR
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value,
            5,
            0,
            test_num | acc_value,
        )  # STA


@cocotb.test()
async def test_ORA_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ad"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            acc_value,
        )  # LDA
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("0d"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            4,
            test_num,
        )  # OR
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value_LB,
            7,
            0,
            test_num | acc_value,
        )  # STA


@cocotb.test()
async def test_ORA_IMM_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ad"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            acc_value,
        )  # LDA
        await helper.run_input_imm_instruction(
            dut,
            helper.hex_to_num("09"),
            4,
            test_num,
        )  # OR Imm
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value_LB,
            6,
            0,
            test_num | acc_value,
        )  # STA


@cocotb.test()
async def test_EOR_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, acc_value
        )  # LDA ZPG
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("45"), memory_addr_with_value, 3, test_num
        )  # EOR ZPG
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value,
            5,
            0,
            test_num ^ acc_value,
        )  # STA ZPG


@cocotb.test()
async def test_EOR_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ad"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            acc_value,
        )  # LDA
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("4d"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            4,
            test_num,
        )  # EOR
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value_LB,
            7,
            0,
            test_num ^ acc_value,
        )  # STA


@cocotb.test()
async def test_EOR_IMM_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ad"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            acc_value,
        )  # LDA
        await helper.run_input_imm_instruction(
            dut,
            helper.hex_to_num("49"),
            4,
            test_num,
        )  # EOR Imm
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value_LB,
            6,
            0,
            test_num ^ acc_value,
        )  # STA


@cocotb.test()
async def test_CPX_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)

        # just make sure it always branches
        x_value = random.randint(50, 255)
        test_value = random.randint(10, 49)
        branch_amount = random.randint(1, 50)

        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ae"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            x_value,
        )  # LDX ABS
        await helper.run_input_zpg_instruction(
            dut,
            helper.hex_to_num("e4"),
            memory_addr_with_value_LB,
            4,
            test_value,
        )  # CPX ZPG
        await helper.test_branch_instruction(
            dut,
            helper.hex_to_num("b0"),
            6,
            branch_amount,
        )  # BCS REL
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("86"),
            memory_addr_with_value_LB,
            7 + branch_amount,
            0,
            x_value,
        )  # STX ZPG


@cocotb.test()
async def test_CPX_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)

        # just make sure it always branches
        x_value = random.randint(50, 255)
        test_value = random.randint(10, 49)
        branch_amount = random.randint(1, 50)

        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ae"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            x_value,
        )  # LDX ABS
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ec"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            4,
            test_value,
        )  # CPX ABS
        await helper.test_branch_instruction(
            dut,
            helper.hex_to_num("b0"),
            7,
            branch_amount,
        )  # BCS REL
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("86"),
            memory_addr_with_value_LB,
            8 + branch_amount,
            0,
            x_value,
        )  # STX ZPG


@cocotb.test()
async def test_CPX_IMM_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)

        # just make sure it always branches
        x_value = random.randint(50, 255)
        imm_value = random.randint(10, 49)
        branch_amount = random.randint(1, 50)

        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ae"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            x_value,
        )  # LDX ABS
        await helper.run_input_imm_instruction(
            dut,
            helper.hex_to_num("e0"),
            4,
            imm_value,
        )  # CPX IMM
        await helper.test_branch_instruction(
            dut,
            helper.hex_to_num("b0"),
            6,
            branch_amount,
        )  # BCS REL
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("86"),
            memory_addr_with_value_LB,
            7 + branch_amount,
            0,
            x_value,
        )  # STX ZPG


@cocotb.test()
async def test_CMP_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)

        # just make sure it always branches
        acc_value = random.randint(50, 255)
        test_value = random.randint(10, 49)
        branch_amount = random.randint(1, 50)

        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ad"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            acc_value,
        )  # LDA ABS
        await helper.run_input_zpg_instruction(
            dut,
            helper.hex_to_num("c5"),
            memory_addr_with_value_LB,
            4,
            test_value,
        )  # CMP ZPG
        await helper.test_branch_instruction(
            dut,
            helper.hex_to_num("b0"),
            6,
            branch_amount,
        )  # BCS REL
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value_LB,
            7 + branch_amount,
            0,
            acc_value,
        )  # STA


@cocotb.test()
async def test_CMP_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)

        # just make sure it always branches
        acc_value = random.randint(50, 255)
        test_value = random.randint(10, 49)
        branch_amount = random.randint(1, 50)

        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ad"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            acc_value,
        )  # LDA ABS
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("cd"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            4,
            test_value,
        )  # CMP ABS
        await helper.test_branch_instruction(
            dut,
            helper.hex_to_num("b0"),
            7,
            branch_amount,
        )  # BCS REL
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value_LB,
            8 + branch_amount,
            0,
            acc_value,
        )  # STA


@cocotb.test()
async def test_CMP_IMM_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)

        # just make sure it always branches
        acc_value = random.randint(50, 255)
        imm_value = random.randint(10, 49)
        branch_amount = random.randint(1, 50)

        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ad"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            acc_value,
        )  # LDA ABS
        await helper.run_input_imm_instruction(
            dut,
            helper.hex_to_num("c9"),
            4,
            imm_value,
        )  # CMP IMM
        await helper.test_branch_instruction(
            dut,
            helper.hex_to_num("b0"),
            6,
            branch_amount,
        )  # BCS REL
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value_LB,
            7 + branch_amount,
            0,
            acc_value,
        )  # STA


@cocotb.test()
async def test_CPY_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)

        # just make sure it always branches
        y_value = random.randint(50, 255)
        test_value = random.randint(10, 49)
        branch_amount = random.randint(1, 50)

        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ac"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            y_value,
        )  # LDY ABS
        await helper.run_input_zpg_instruction(
            dut,
            helper.hex_to_num("c4"),
            memory_addr_with_value_LB,
            4,
            test_value,
        )  # CPY ZPG
        await helper.test_branch_instruction(
            dut,
            helper.hex_to_num("b0"),
            6,
            branch_amount,
        )  # BCS REL
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("84"),
            memory_addr_with_value_LB,
            7 + branch_amount,
            0,
            y_value,
        )  # STY ZPG


@cocotb.test()
async def test_CPY_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)

        # just make sure it always branches
        y_value = random.randint(50, 255)
        test_value = random.randint(10, 49)
        branch_amount = random.randint(1, 50)

        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ac"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            y_value,
        )  # LDX ABS
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("cc"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            4,
            test_value,
        )  # CPX ABS
        await helper.test_branch_instruction(
            dut,
            helper.hex_to_num("b0"),
            7,
            branch_amount,
        )  # BCS REL
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("84"),
            memory_addr_with_value_LB,
            8 + branch_amount,
            0,
            y_value,
        )  # STY ZPG


@cocotb.test()
async def test_CPY_IMM_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)

        # just make sure it always branches
        y_value = random.randint(50, 255)
        imm_value = random.randint(10, 49)
        branch_amount = random.randint(1, 50)

        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ac"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            y_value,
        )  # LDY ABS
        await helper.run_input_imm_instruction(
            dut,
            helper.hex_to_num("c0"),
            4,
            imm_value,
        )  # CPY IMM
        await helper.test_branch_instruction(
            dut,
            helper.hex_to_num("b0"),
            6,
            branch_amount,
        )  # BCS REL
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("84"),
            memory_addr_with_value_LB,
            7 + branch_amount,
            0,
            y_value,
        )  # STY ZPG


@cocotb.test()
async def test_ADC_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, acc_value
        )  # LDA
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("65"), memory_addr_with_value, 3, test_num
        )  # ADC
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value,
            5,
            0,
            (test_num + acc_value) % 256,
        )  # STA


@cocotb.test()
async def test_ADC_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ad"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            acc_value,
        )  # LDA
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("6d"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            4,
            test_num,
        )  # ADC
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value_LB,
            7,
            0,
            (test_num + acc_value) % 256,
        )  # STA


@cocotb.test()
async def test_ADC_IMM_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ad"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            acc_value,
        )  # LDA
        await helper.run_input_imm_instruction(
            dut,
            helper.hex_to_num("69"),
            4,
            test_num,
        )  # OR Imm
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value_LB,
            6,
            0,
            (test_num + acc_value) % 256,
        )  # STA


@cocotb.test()
async def test_SBC_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, acc_value
        )  # LDA ZPG
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("e5"), memory_addr_with_value, 3, test_num
        )  # SBC ZPG
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value,
            5,
            0,
            (test_num - acc_value) % 256,
        )  # STA ZPG


@cocotb.test()
async def test_SBC_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_HB = random.randint(10, 255)
        memory_addr_with_value_LB = random.randint(10, 255)

        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ad"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            acc_value,
        )  # LDA ABS
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ed"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            4,
            test_num,
        )  # SBC ABS
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value_LB,
            7,
            0,
            (test_num - acc_value) % 256,
        )  # STA ZPG


@cocotb.test()
async def test_SBC_IMM_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut,
            helper.hex_to_num("ad"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            acc_value,
        )  # LDA ABS
        await helper.run_input_imm_instruction(
            dut,
            helper.hex_to_num("e9"),
            4,
            test_num,
        )  # SBC IMM
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value_LB,
            6,
            0,
            (test_num - acc_value) % 256,
        )  # STA ZPG


@cocotb.test()
async def test_INC_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("e6"),
            memory_addr_with_value,
            1,
            test_num,
            (test_num + 1) % 256,
        )  # INC ZPG


@cocotb.test()
async def test_INC_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_HB = random.randint(10, 255)
        memory_addr_with_value_LB = random.randint(10, 255)

        await helper.reset_cpu(dut)
        await helper.test_abs_instruction(
            dut,
            helper.hex_to_num("ee"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            test_num,
            (test_num + 1) % 256,
        )  # INC ABS


@cocotb.test()
async def test_DEC_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("c6"),
            memory_addr_with_value,
            1,
            test_num,
            (test_num - 1) % 256,
        )  # DEC ZPG


@cocotb.test()
async def test_DEC_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_HB = random.randint(10, 255)
        memory_addr_with_value_LB = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.test_abs_instruction(
            dut,
            helper.hex_to_num("ce"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            1,
            test_num,
            (test_num - 1) % 256,
        )  # DEC ABS


@cocotb.test()
async def test_JMP_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        goal_HB = random.randint(1, 255)
        memory_addr_with_value_LB = random.randint(10, 255)
        goal_LB = test_num
        goal = goal_HB * 256 + goal_LB
        await helper.reset_cpu(dut)
        await helper.run_jmp_abs_instruction(
            dut,
            helper.hex_to_num("4c"),
            goal_HB,
            goal_LB,
            1,
        )
        test_num = 69

        await helper.test_zpg_instruction_jmp_specifc(
            dut,
            helper.hex_to_num("06"),
            memory_addr_with_value_LB,
            goal,
            test_num,
            (test_num * 2) % 256,
        )


@cocotb.test()
async def test_BCS_REL_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM - 4):
        memory_addr_for_verify = random.randint(10, 255)

        await helper.reset_cpu(dut)

        await helper.test_impl_instruction(
            dut,
            helper.hex_to_num("38"),  # Set Carry
            1,
        )

        await helper.test_branch_instruction(dut, helper.hex_to_num("b0"), 2, test_num)
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("06"),
            memory_addr_for_verify,
            3 + test_num,
            test_num,
            (test_num * 2) % 256,
        )


@cocotb.test()
async def test_BCC_REL_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM - 4):
        memory_addr_for_verify = random.randint(10, 255)

        await helper.reset_cpu(dut)

        await helper.test_impl_instruction(
            dut,
            helper.hex_to_num("38"),  # Set Carry
            1,
        )
        await helper.test_impl_instruction(
            dut,
            helper.hex_to_num("18"),  # Clear Carry
            2,
        )
        await helper.test_branch_instruction(dut, helper.hex_to_num("90"), 3, test_num)
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("06"),
            memory_addr_for_verify,
            4 + test_num,
            test_num,
            (test_num * 2) % 256,
        )


@cocotb.test()
async def test_BEQ_REL_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM - 5):
        memory_addr_for_verify = random.randint(10, 255)

        await helper.reset_cpu(dut)

        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, 0
        )  # LDA
        await helper.run_transfer_instruction(dut, helper.hex_to_num("aa"), 3)  # TAX
        await helper.test_branch_instruction(dut, helper.hex_to_num("f0"), 4, test_num)
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("06"),
            memory_addr_for_verify,
            5 + test_num,
            test_num,
            (test_num * 2) % 256,
        )


@cocotb.test()
async def test_BNE_REL_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM - 4):
        memory_addr_for_verify = random.randint(10, 255)

        await helper.reset_cpu(dut)

        await helper.test_branch_instruction(dut, helper.hex_to_num("d0"), 1, test_num)
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("06"),
            memory_addr_for_verify,
            2 + test_num,
            test_num,
            (test_num * 2) % 256,
        )


@cocotb.test()
async def test_BPL_REL_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM - 4):
        memory_addr_for_verify = random.randint(10, 255)

        await helper.reset_cpu(dut)

        await helper.test_branch_instruction(dut, helper.hex_to_num("10"), 1, test_num)
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("06"),
            memory_addr_for_verify,
            2 + test_num,
            test_num,
            (test_num * 2) % 256,
        )


@cocotb.test()
async def test_BMI_REL_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM - 4):
        memory_addr_for_verify = random.randint(10, 255)

        await helper.reset_cpu(dut)

        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, 255
        )  # LDA
        test_num = 10
        await helper.test_branch_instruction(dut, helper.hex_to_num("30"), 3, test_num)
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("06"),
            memory_addr_for_verify,
            4 + test_num,
            test_num,
            (test_num * 2) % 256,
        )


@cocotb.test()
async def test_INX_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a6"), memory_addr_with_value, 1, test_num
        )  # LDX
        await helper.run_incXY_instruction(dut, helper.hex_to_num("e8"), 3)  # INX
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("86"),
            memory_addr_with_value,
            4,
            0,
            (test_num + 1) % 256,
        )  # STX


@cocotb.test()
async def test_INY_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a4"), memory_addr_with_value, 1, test_num
        )  # LDY
        await helper.run_incXY_instruction(dut, helper.hex_to_num("c8"), 3)  # INY
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("84"),
            memory_addr_with_value,
            4,
            0,
            (test_num + 1) % 256,
        )  # STY


@cocotb.test()
async def test_DEX_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a6"), memory_addr_with_value, 1, test_num
        )  # LDX
        await helper.run_incXY_instruction(dut, helper.hex_to_num("ca"), 3)  # DEX
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("86"),
            memory_addr_with_value,
            4,
            0,
            (test_num - 1) % 256,
        )  # STX


@cocotb.test()
async def test_DEY_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a4"), memory_addr_with_value, 1, test_num
        )  # LDY
        await helper.run_incXY_instruction(dut, helper.hex_to_num("88"), 3)  # DEY
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("84"),
            memory_addr_with_value,
            4,
            0,
            (test_num - 1) % 256,
        )  # STY


@cocotb.test()
async def test_ASL_A_ZPG_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, test_num
        )  # LDA
        await helper.run_incXY_instruction(dut, helper.hex_to_num("0a"), 3)  # ASL A
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value,
            4,
            0,
            (test_num * 2) % 256,
        )  # STA


@cocotb.test()
async def test_LSR_A_ZPG_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, test_num
        )  # LDA
        await helper.run_incXY_instruction(dut, helper.hex_to_num("4a"), 3)  # ASL A
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value,
            4,
            0,
            (test_num // 2) % 256,
        )  # STA


@cocotb.test()
async def test_ROL_A_ZPG_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, test_num
        )  # LDA
        await helper.run_incXY_instruction(dut, helper.hex_to_num("2a"), 3)  # ASL A
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value,
            4,
            0,
            (test_num * 2) % 256 + test_num // 128,
        )  # STA


@cocotb.test()
async def test_ROR_A_ZPG_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, test_num
        )  # LDA
        await helper.run_incXY_instruction(dut, helper.hex_to_num("6a"), 3)  # ASL A
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value,
            4,
            0,
            (test_num // 2) % 256 + (test_num % 2) * 128,
        )  # STA


@cocotb.test()
async def test_TAX_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, test_num
        )  # LDA
        await helper.run_transfer_instruction(dut, helper.hex_to_num("aa"), 3)  # TAX
        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("86"), memory_addr_with_value, 4, 0, test_num
        )  # STX


@cocotb.test()
async def test_TAY_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, test_num
        )  # LDA
        await helper.run_transfer_instruction(dut, helper.hex_to_num("a8"), 3)  # TAY
        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("84"), memory_addr_with_value, 4, 0, test_num
        )  # STY


@cocotb.test()
async def test_TXA_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a6"), memory_addr_with_value, 1, test_num
        )  # LDX
        await helper.run_transfer_instruction(dut, helper.hex_to_num("8a"), 3)  # TXA
        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("85"), memory_addr_with_value, 4, 0, test_num
        )  # STA


@cocotb.test()
async def test_TYA_Base(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a4"), memory_addr_with_value, 1, test_num
        )  # LDY
        await helper.run_transfer_instruction(dut, helper.hex_to_num("98"), 3)  # TYA
        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("85"), memory_addr_with_value, 4, 0, test_num
        )  # STA


@cocotb.test()
async def test_all_load_transfer_store_fuzz(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for _ in range(MAX_TESTS):
        await helper.reset_cpu(dut)
        register_state = [0, 0, 0]
        pc = 1

        while pc < 230:
            # Randomly load
            if random.random() > 0.5:
                val = random.randint(0, 255)
                register_state[0] = val
                await helper.run_input_zpg_instruction(
                    dut, helper.hex_to_num("a6"), 251, pc, val
                )  # LDX
                pc += 2
            if random.random() > 0.5:
                val = random.randint(0, 255)
                register_state[1] = val
                await helper.run_input_zpg_instruction(
                    dut, helper.hex_to_num("a4"), 251, pc, val
                )  # LDY
                pc += 2
            if random.random() > 0.5:
                val = random.randint(0, 255)
                register_state[2] = val
                await helper.run_input_zpg_instruction(
                    dut, helper.hex_to_num("a5"), 251, pc, val
                )  # LDA
                pc += 2

            # randomly swap
            if random.random() > 0.5:
                register_state[2] = register_state[0]
                await helper.run_transfer_instruction(
                    dut, helper.hex_to_num("8a"), pc
                )  # TXA
                pc += 1
            # randomly swap
            if random.random() > 0.5:
                register_state[0] = register_state[2]
                await helper.run_transfer_instruction(
                    dut, helper.hex_to_num("aa"), pc
                )  # TAX
                pc += 1
            # randomly swap
            if random.random() > 0.5:
                register_state[2] = register_state[1]
                await helper.run_transfer_instruction(
                    dut, helper.hex_to_num("98"), pc
                )  # TYA
                pc += 1
            # randomly swap
            if random.random() > 0.5:
                register_state[1] = register_state[2]
                await helper.run_transfer_instruction(
                    dut, helper.hex_to_num("a8"), pc
                )  # TAY
                pc += 1

            # check the X, Y and A values
            await helper.test_zpg_instruction(
                dut, helper.hex_to_num("86"), 250, pc, 0, register_state[0]
            )  # STX
            pc += 2
            await helper.test_zpg_instruction(
                dut, helper.hex_to_num("84"), 250, pc, 0, register_state[1]
            )  # STY
            pc += 2
            await helper.test_zpg_instruction(
                dut, helper.hex_to_num("85"), 250, pc, 0, register_state[2]
            )  # STA
            pc += 2


@cocotb.test()
async def test_add_matrix_fuzz(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for _ in range(MAX_TESTS):
        await helper.reset_cpu(dut)

        memory_page_0 = [
            helper.hex_to_num("ea"),  # NOP
            helper.hex_to_num("a2"),  # LDX IMM
            0,
            helper.hex_to_num("6d"),  # ADC ABS
            5,
            0,
            helper.hex_to_num("6d"),  # ADC ABS
            6,
            0,
            helper.hex_to_num("8d"),  # STA ABS
            7,
            0,
            helper.hex_to_num("a9"),  # LDA IMM
            0,
            helper.hex_to_num("e8"),  # INX
            helper.hex_to_num("86"),  # STX ZPG
            5,
            helper.hex_to_num("86"),  # STX ZPG
            8,
            helper.hex_to_num("86"),  # STX ZPG
            11,
            helper.hex_to_num("4c"),  # JMP ABS
            0,
            3,
        ]
        memory_page_5 = [random.randint(1, 255) for _ in range(256)]
        memory_page_6 = [random.randint(1, 255) for _ in range(256)]
        memory_page_7 = [0 for _ in range(256)]

        # set x to be 0
        await helper.test_imm_instruction(
            dut, memory_page_0[1], 1, memory_page_0[2]
        )  # LDX_IMM 0
        x = 0

        for _ in range(256):
            await helper.run_input_abs_instruction(
                dut,
                memory_page_0[3],
                memory_page_0[4],
                memory_page_0[5],
                3,
                memory_page_5[x],
            )  # ADC
            await helper.run_input_abs_instruction(
                dut,
                memory_page_0[6],
                memory_page_0[7],
                memory_page_0[8],
                6,
                memory_page_6[x],
            )  # ADC
            await helper.test_abs_instruction(
                dut,
                memory_page_0[9],
                memory_page_0[10],
                memory_page_0[11],
                9,
                0,  # no input
                (memory_page_5[x] + memory_page_6[x]) % 256,
            )  # STA ABS
            memory_page_7[x] = (memory_page_5[x] + memory_page_6[x]) % 256
            await helper.test_imm_instruction(
                dut, memory_page_0[12], 12, memory_page_0[13]
            )  # LDA_IMM 0
            await helper.run_incXY_instruction(dut, memory_page_0[14], 14)  # INX
            x += 1
            x %= 256

            # now we edit the program with the info we want

            await helper.test_zpg_instruction(
                dut, memory_page_0[15], memory_page_0[16], 15, 0, x
            )  # STX
            memory_page_0[memory_page_0[16]] = x

            await helper.test_zpg_instruction(
                dut, memory_page_0[17], memory_page_0[18], 17, 0, x
            )  # STX
            memory_page_0[memory_page_0[18]] = x

            await helper.test_zpg_instruction(
                dut, memory_page_0[19], memory_page_0[20], 19, 0, x
            )  # STX
            memory_page_0[memory_page_0[20]] = x

            # now jump to the start of the program
            await helper.run_jmp_abs_instruction(
                dut,
                memory_page_0[21],
                memory_page_0[22],
                memory_page_0[23],
                21,
            )

        # now we check the final matrix
        for i in range(256):
            assert (memory_page_5[i] + memory_page_6[i]) % 256 == memory_page_7[i]


@cocotb.test()
async def test_multiply_nums_fuzz(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    for _ in range(MAX_TESTS):
        await helper.reset_cpu(dut)

        # initialize memory page 0
        memory_page_0 = [0 for _ in range(256)]

        memory_page_0[0] = helper.hex_to_num("ea")  # NOP

        memory_page_0[1] = helper.hex_to_num("c5")  # CMP ZPG
        memory_page_0[2] = 251

        memory_page_0[3] = helper.hex_to_num("d0")  # BNE
        memory_page_0[4] = 4

        # Jump if the second number is 0
        memory_page_0[5] = helper.hex_to_num("4c")  # JMP ABS
        memory_page_0[6] = 0
        memory_page_0[7] = 100

        # if the second number is not 0
        memory_page_0[8] = helper.hex_to_num("65")  # ADC ZPG
        memory_page_0[9] = 250
        memory_page_0[10] = helper.hex_to_num("c6")  # DEC ZPG
        memory_page_0[11] = 251

        # return to the start
        memory_page_0[12] = helper.hex_to_num("4c")  # JMP ABS
        memory_page_0[13] = 0
        memory_page_0[14] = 3

        # Output Value
        memory_page_0[100] = helper.hex_to_num("85")  # ADC ZPG
        memory_page_0[101] = 252

        # Trap Self meant to emulate the rest of the program
        memory_page_0[102] = helper.hex_to_num("4c")  # JMP ABS
        memory_page_0[103] = 0
        memory_page_0[104] = 102

        # starting nums
        memory_page_0[250] = random.randint(0, 255)
        memory_page_0[251] = random.randint(0, 255)
        memory_page_0[252] = 0

        a = memory_page_0[250]
        b = memory_page_0[251]
        acc = 0
        t = 0

        await helper.run_input_zpg_instruction(
            dut,
            memory_page_0[1],
            memory_page_0[2],
            1,
            memory_page_0[memory_page_0[2]],
        )  # CPX ZPG

        while t < 500:  # guarantee that the number is multiplied by the end
            await helper.test_branch_instruction(
                dut, memory_page_0[3], 3, memory_page_0[4]
            )
            if memory_page_0[251] == 0:
                await helper.run_jmp_abs_instruction(
                    dut,
                    memory_page_0[5],
                    memory_page_0[6],
                    memory_page_0[7],
                    5,
                )

                await helper.test_zpg_instruction(
                    dut, memory_page_0[100], memory_page_0[101], 100, 0, (a * b) % 256
                )  # STA
                memory_page_0[252] = (a * b) % 256

                for _ in range(5):
                    await helper.run_jmp_abs_instruction(
                        dut,
                        memory_page_0[102],
                        memory_page_0[103],
                        memory_page_0[104],
                        102,
                    )  # let the jump run a few times

                t = 1000
            else:
                await helper.run_input_zpg_instruction(
                    dut,
                    memory_page_0[8],
                    memory_page_0[9],
                    8,
                    memory_page_0[memory_page_0[9]],
                )  # ADC
                acc += a
                await helper.test_zpg_instruction(
                    dut,
                    memory_page_0[10],
                    memory_page_0[11],
                    10,
                    memory_page_0[memory_page_0[11]],
                    (memory_page_0[251] - 1) % 256,
                )  # DEC ZPG
                memory_page_0[251] -= 1
                memory_page_0[251] %= 256
                await helper.run_jmp_abs_instruction(
                    dut,
                    memory_page_0[12],
                    memory_page_0[13],
                    memory_page_0[14],
                    12,
                )
            t += 1
        assert memory_page_0[252] == (a * b) % 256
