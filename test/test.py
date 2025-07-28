# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
import random

import helper

MAX_TESTS = 31  # for the fuzz tests
MAX_TEST_NUM = 255  # for the instruction specific tests


@cocotb.test()
async def test_ASL_ZPG_Clear(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value_HB = random.randint(10, 255)
        memory_addr_with_value_LB = random.randint(10, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut, helper.hex_to_num("ae"), memory_addr_with_value_HB, memory_addr_with_value_LB, 1, test_num
        ) # LDX ABS
        await helper.test_abs_instruction(
            dut, helper.hex_to_num("8e"), memory_addr_with_value_HB, memory_addr_with_value_LB, 4, 0, test_num
        ) # STX ABS

@cocotb.test()
async def test_LDX_IMM_Base(dut):
    clock = Clock(dut.clk, 50, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_for_verify = random.randint(10, 255)

        await helper.reset_cpu(dut)

        await helper.test_imm_instruction(dut, helper.hex_to_num("a2"), 1, test_num)

        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("86"), memory_addr_for_verify, 2, 0, test_num
        )


@cocotb.test()
async def test_LDA_ZPG_Base(dut):
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)

        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut, helper.hex_to_num("ad"), memory_addr_with_value_HB, memory_addr_with_value_LB, 1, test_num
        ) #LDA ABS
        await helper.test_abs_instruction(
            dut, helper.hex_to_num("8d"), memory_addr_with_value_HB, memory_addr_with_value_LB, 4, 0, test_num
        ) #STA ABS

@cocotb.test()
async def test_LDA_IMM_Base(dut):
    clock = Clock(dut.clk, 50, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_for_verify = random.randint(10, 255)

        await helper.reset_cpu(dut)

        await helper.test_imm_instruction(dut, helper.hex_to_num("a9"), 1, test_num)

        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("85"), memory_addr_for_verify, 2, 0, test_num
        )


@cocotb.test()
async def test_LDY_ZPG_Base(dut):
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
        ) # LDY ABS
        await helper.test_abs_instruction(
            dut,
            helper.hex_to_num("8c"),
            memory_addr_with_value_HB,
            memory_addr_with_value_LB,
            4,
            0,
            test_num,
        ) # STY ABS


@cocotb.test()
async def test_LDY_IMM_Base(dut):
    clock = Clock(dut.clk, 50, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(1, MAX_TEST_NUM):
        memory_addr_for_verify = random.randint(10, 255)

        await helper.reset_cpu(dut)

        await helper.test_imm_instruction(dut, helper.hex_to_num("a0"), 1, test_num)

        await helper.test_zpg_instruction(
            dut, helper.hex_to_num("84"), memory_addr_for_verify, 2, 0, test_num
        )


@cocotb.test()
async def test_AND_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut, helper.hex_to_num("ad"), memory_addr_with_value_HB, memory_addr_with_value_LB, 1, acc_value
        )  # LDA
        await helper.run_input_abs_instruction(
            dut, helper.hex_to_num("2d"), memory_addr_with_value_HB, memory_addr_with_value_LB, 4, test_num
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
async def test_ORA_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
async def test_EOR_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 50, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("a5"), memory_addr_with_value, 1, acc_value
        )  # LDA
        await helper.run_input_zpg_instruction(
            dut, helper.hex_to_num("45"), memory_addr_with_value, 3, test_num
        )  # EOR
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value,
            5,
            0,
            test_num ^ acc_value,
        )  # STA

@cocotb.test()
async def test_EOR_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 50, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut, helper.hex_to_num("ad"), memory_addr_with_value_HB, memory_addr_with_value_LB, 1, acc_value
        )  # LDA
        await helper.run_input_abs_instruction(
            dut, helper.hex_to_num("4d"), memory_addr_with_value_HB, memory_addr_with_value_LB, 4, test_num
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
async def test_ADC_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        memory_addr_with_value_LB = random.randint(10, 255)
        memory_addr_with_value_HB = random.randint(10, 255)
        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut, helper.hex_to_num("ad"), memory_addr_with_value_HB, memory_addr_with_value_LB, 1, acc_value
        )  # LDA
        await helper.run_input_abs_instruction(
            dut, helper.hex_to_num("6d"), memory_addr_with_value_HB, memory_addr_with_value_LB, 4, test_num
        )  # EOR
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value_LB,
            7,
            0,
            (test_num + acc_value)%256,
        )  # STA

@cocotb.test()
async def test_SBC_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 50, units="ns")
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
            (test_num - acc_value)%256,
        )  # STA ZPG

@cocotb.test()
async def test_SBC_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 50, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(256):
        memory_addr_with_value_HB = random.randint(10, 255)
        memory_addr_with_value_LB = random.randint(10, 255)

        acc_value = random.randint(0, 255)
        await helper.reset_cpu(dut)
        await helper.run_input_abs_instruction(
            dut, helper.hex_to_num("ad"), memory_addr_with_value_HB, memory_addr_with_value_LB, 1, acc_value
        )  # LDA ABS
        await helper.run_input_abs_instruction(
            dut, helper.hex_to_num("ed"), memory_addr_with_value_HB, memory_addr_with_value_LB, 4, test_num
        )  # SBC ABS
        await helper.test_zpg_instruction(
            dut,
            helper.hex_to_num("85"),
            memory_addr_with_value_LB,
            7,
            0,
            (test_num - acc_value)%256,
        )  # STA ZPG

@cocotb.test()
async def test_INC_ZPG_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
async def test_DEC_ABS_Base(dut):
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TEST_NUM):
        goal_HB = random.randint(1, 255)
        memory_addr_with_value_LB = random.randint(10, 255)
        goal_LB = test_num
        memory_addr_with_value_HB = random.randint(1, 255)
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
async def test_INX_Base(dut):
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
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
    clock = Clock(dut.clk, 50, units="ns")
    cocotb.start_soon(clock.start())

    for test_num in range(MAX_TESTS):
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
