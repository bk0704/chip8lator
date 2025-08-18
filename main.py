# ============================================================
# CHIP-8 Opcode Test Runner (for your current CPU implementation)
# Paste at bottom of main.py (or run as a separate script)
# ============================================================
import cpu

TOTAL = 0
PASS  = 0

def ok(name, cond, extra=""):
    global TOTAL, PASS
    TOTAL += 1
    if cond:
        PASS += 1
        print(f"[{name}] PASS {extra}")
    else:
        print(f"[{name}] FAIL {extra}")

def fresh():
    return cpu.CPU()

def write_opcode(c, addr, opcode):
    c.memory[addr]     = (opcode >> 8) & 0xFF
    c.memory[addr + 1] = opcode & 0xFF

def run_once(c, opcode):
    c.memory[c.PC] = (opcode >> 8) & 0xFF
    c.memory[c.PC + 1] = opcode & 0xFF
    fetched = c.fetch_opcode()
    c.decode_and_execute(fetched)
    return fetched


# ---------- Tests ----------

def test_fetch_opcode():
    c = fresh()
    c.memory[0x200] = 0xA2
    c.memory[0x201] = 0xF0
    op = c.fetch_opcode()
    ok("fetch_opcode", op == 0xA2F0, f"(got={hex(op)})")

def test_6XNN_set():
    c = fresh()
    run_once(c, 0x60AB)  # V0=0xAB
    ok("6XNN", c.V[0] == 0xAB and c.PC == 0x202, f"(V0={c.V[0]}, PC={hex(c.PC)})")

def test_7XNN_add_wrap():
    c = fresh(); c.V[1] = 250
    run_once(c, 0x710F)  # V1 += 15 => 265 -> 9
    ok("7XNN wrap", c.V[1] == 9 and c.PC == 0x202, f"(V1={c.V[1]})")

def test_8XY0_mov():
    c = fresh(); c.V[2]=0x11; c.V[3]=0x77
    run_once(c, 0x8230)  # V2 = V3
    ok("8XY0 mov", c.V[2]==0x77, f"(V2={c.V[2]})")

def test_logic_or_and_xor():
    # OR
    c = fresh(); c.V[4]=0b10100000; c.V[5]=0b00001111
    run_once(c, 0x8451)
    or_ok = (c.V[4] == 0b10101111)
    # AND
    c = fresh(); c.V[4]=0b10101010; c.V[5]=0b11001100
    run_once(c, 0x8452)
    and_ok = (c.V[4] == 0b10001000)
    # XOR
    c = fresh(); c.V[4]=0b10101010; c.V[5]=0b11001100
    run_once(c, 0x8453)
    xor_ok = (c.V[4] == 0b01100110)
    ok("8XY1 OR",  or_ok)
    ok("8XY2 AND", and_ok)
    ok("8XY3 XOR", xor_ok)

def test_8XY4_add_carry():
    # no carry
    c = fresh(); c.V[1]=10; c.V[2]=20
    run_once(c, 0x8124)
    a = (c.V[1]==30 and c.V[0xF]==0)
    # edge 254+1=255 (no carry)
    c = fresh(); c.V[1]=0xFE; c.V[2]=0x01
    run_once(c, 0x8124)
    b = (c.V[1]==0xFF and c.V[0xF]==0)
    # 255+1 -> 0 with carry
    c = fresh(); c.V[1]=0xFF; c.V[2]=0x01
    run_once(c, 0x8124)
    c_ok = (c.V[1]==0x00 and c.V[0xF]==1)
    # 200+100=300 -> 44 with carry
    c = fresh(); c.V[1]=200; c.V[2]=100
    run_once(c, 0x8124)
    d = (c.V[1]==44 and c.V[0xF]==1)
    ok("8XY4 add+carry", a and b and c_ok and d, f"(A={a},B={b},C={c_ok},D={d})")

def test_8XY5_sub_notborrow():
    # no borrow
    c = fresh(); c.V[4]=10; c.V[5]=3
    run_once(c, 0x8455)
    a = (c.V[4]==7 and c.V[0xF]==1)
    # borrow
    c = fresh(); c.V[4]=3; c.V[5]=10
    run_once(c, 0x8455)
    b = (c.V[4]==249 and c.V[0xF]==0)
    ok("8XY5 sub", a and b, f"(no_borrow={a}, borrow={b})")

def test_8XY7_revsub():
    # no borrow: Vy-Vx
    c = fresh(); c.V[6]=3; c.V[7]=10
    run_once(c, 0x8677)
    a = (c.V[6]==7 and c.V[0xF]==1)
    # borrow
    c = fresh(); c.V[6]=10; c.V[7]=3
    run_once(c, 0x8677)
    b = (c.V[6]==249 and c.V[0xF]==0)
    ok("8XY7 revsub", a and b, f"(no_borrow={a}, borrow={b})")

def test_8XY6_shr():
    c = fresh(); c.V[0xC] = 0b00000101  # LSB=1
    run_once(c, 0x8CC6)
    a = (c.V[0xC] == 0b00000010 and c.V[0xF] == 1)
    c = fresh(); c.V[0xC] = 0b00000100  # LSB=0
    run_once(c, 0x8CC6)
    b = (c.V[0xC] == 0b00000010 and c.V[0xF] == 0)
    ok("8XY6 SHR", a and b, f"(lsb1={a}, lsb0={b})")

def test_8XYE_shl():
    c = fresh(); c.V[0xD] = 0b10000001  # MSB=1
    run_once(c, 0x8DCE)
    a = (c.V[0xD] == 0b00000010 and c.V[0xF] == 1)  # 0x81<<1 = 0x102 -> 0x02, carry=1
    c = fresh(); c.V[0xD] = 0b01000001  # MSB=0
    run_once(c, 0x8DCE)
    b = (c.V[0xD] == 0b10000010 and c.V[0xF] == 0)
    ok("8XYE SHL", a and b, f"(msb1={a}, msb0={b})")

def test_3XNN_skip_eq():
    c = fresh(); c.V[1]=0x20
    write_opcode(c, 0x202, 0x6000)  # harmless next
    run_once(c, 0x3120)
    ok("3XNN skip eq", c.PC == 0x204, f"(PC={hex(c.PC)})")

def test_4XNN_skip_neq():
    c = fresh(); c.V[1]=0x20
    write_opcode(c, 0x202, 0x6000)
    run_once(c, 0x4121)
    ok("4XNN skip neq", c.PC == 0x204, f"(PC={hex(c.PC)})")

def test_5XY0_skip_equal_strict():
    c = fresh(); c.V[8]=42; c.V[9]=42
    write_opcode(c, 0x202, 0x6000)
    run_once(c, 0x5890)
    ok("5XY0 skip eq", c.PC == 0x204, f"(PC={hex(c.PC)})")

def test_9XY0_skip_notequal_strict():
    c = fresh(); c.V[0xA]=1; c.V[0xB]=2
    write_opcode(c, 0x202, 0x6000)
    run_once(c, 0x9AB0)
    ok("9XY0 skip neq", c.PC == 0x204, f"(PC={hex(c.PC)})")

def test_1NNN_jump():
    c = fresh()
    run_once(c, 0x1200)  # jump to 0x200
    ok("1NNN jump", c.PC == 0x200, f"(PC={hex(c.PC)})")

def test_2NNN_call_and_00EE_ret():
    c = fresh()
    # Place: 200: 2204 (CALL 0x204); 202: NOP; 204: 00EE (RET)
    write_opcode(c, 0x200, 0x2204)
    write_opcode(c, 0x204, 0x00EE)
    fetched = c.fetch_opcode(); c.decode_and_execute(fetched)
    a = (c.PC == 0x204 and c.stack and c.stack[-1] == 0x200)
    fetched = c.fetch_opcode(); c.decode_and_execute(fetched)
    b = (c.PC == 0x202 and len(c.stack) == 0)
    ok("2NNN call", a, f"(PC={hex(c.PC)})")
    ok("00EE ret", b)

def test_ANNN_setI():
    c = fresh()
    run_once(c, 0xA2F0)
    ok("ANNN set I", c.i == 0x2F0, f"(I={hex(c.i)})")

def test_00E0_clear():
    c = fresh()
    # Fill screen
    for y in range(32):
        for x in range(64):
            c.display[y][x] = 1
    run_once(c, 0x00E0)
    cleared = all(px == 0 for row in c.display for px in row)
    ok("00E0 clear", cleared and c.PC == 0x202, f"(PC={hex(c.PC)})")

def test_DXYN_draw_and_collision():
    c = fresh()
    # Sprite: 11110000 at I=0x300
    c.i = 0x300; c.memory[0x300] = 0xF0
    c.V[0]=2; c.V[1]=1  # (x=2,y=1)
    run_once(c, 0xD011)  # draw N=1 row
    first_vf = (c.V[0xF] == 0)
    first_pixels = (c.display[1][2:10] == [1,1,1,1,0,0,0,0])
    # Draw same again => toggle off, VF=1
    run_once(c, 0xD011)
    second_vf = (c.V[0xF] == 1)
    second_pixels = (c.display[1][2:10] == [0,0,0,0,0,0,0,0])
    ok("DXYN draw/collision", first_vf and first_pixels and second_vf and second_pixels,
       f"(VF1={first_vf}, VF2={second_vf})")

def test_EX_skips():
    # EXA1 skip if NOT pressed
    c = fresh(); c.V[4]=7; c.keys[7]=0
    write_opcode(c, 0x202, 0x6000)
    run_once(c, 0xE4A1)
    a = (c.PC == 0x204)
    # EXA1 no skip when pressed
    c = fresh(); c.V[4]=7; c.keys[7]=1
    run_once(c, 0xE4A1)
    b = (c.PC == 0x202)
    # EX9E skip if pressed
    c = fresh(); c.V[4]=7; c.keys[7]=1
    write_opcode(c, 0x202, 0x6000)
    run_once(c, 0xE49E)
    c_ok = (c.PC == 0x204)
    # EX9E no skip when not pressed
    c = fresh(); c.V[4]=7; c.keys[7]=0
    run_once(c, 0xE49E)
    d = (c.PC == 0x202)
    ok("EXA1 skip !pressed", a, f"(PC={hex(c.PC)})")
    ok("EXA1 no-skip when pressed", b)
    ok("EX9E skip pressed", c_ok)
    ok("EX9E no-skip when !pressed", d)

def test_FX07_read_delay():
    c = fresh()
    c.delay = 37
    # Use V3 for this test: FX07 with X=3 -> 0xF307
    run_once(c, 0xF307)
    ok("FX07 read delay", (c.V[3] == 37) and (c.PC == 0x202),
       f"(V3={c.V[3]}, delay={c.delay}, PC={hex(c.PC)})")

def test_FX15_set_delay():
    c = fresh()
    c.V[5] = 50
    # FX15 with X=5 -> 0xF515
    run_once(c, 0xF515)
    ok("FX15 set delay", (c.delay == 50) and (c.PC == 0x202),
       f"(delay={c.delay}, PC={hex(c.PC)})")

def test_FX18_set_sound():
    c = fresh()
    c.V[6] = 20
    # FX18 with X=6 -> 0xF618
    run_once(c, 0xF618)
    ok("FX18 set sound", (c.sound == 20) and (c.PC == 0x202),
       f"(sound={c.sound}, PC={hex(c.PC)})")

def test_CXNN_random_mask():
    c = fresh()
    X = 3
    NN = 0x0F
    opcode = 0xC300 | NN   # CxNN with x=3, NN=0x0F

    # Run it multiple times to check masking
    all_masked = True
    saw_variety = False
    prev_val = None

    for _ in range(50):
        run_once(c, opcode)
        val = c.V[X]
        if val & 0xF0:  # should never have upper bits set
            all_masked = False
        if prev_val is not None and val != prev_val:
            saw_variety = True
        prev_val = val

    ok("CXNN random mask", all_masked and saw_variety,
       f"(masked={all_masked}, varied={saw_variety})")


def run_all():
    print("Running CHIP-8 opcode tests...\n")
    test_fetch_opcode()
    test_6XNN_set()
    test_7XNN_add_wrap()
    test_8XY0_mov()
    test_logic_or_and_xor()
    test_8XY4_add_carry()
    test_8XY5_sub_notborrow()
    test_8XY7_revsub()
    test_8XY6_shr()
    test_8XYE_shl()
    test_3XNN_skip_eq()
    test_4XNN_skip_neq()
    test_5XY0_skip_equal_strict()
    test_9XY0_skip_notequal_strict()
    test_1NNN_jump()
    test_2NNN_call_and_00EE_ret()
    test_ANNN_setI()
    test_00E0_clear()
    test_DXYN_draw_and_collision()
    test_EX_skips()
    test_FX07_read_delay()
    test_FX15_set_delay()
    test_FX18_set_sound()
    test_CXNN_random_mask()
    print(f"\nDone. {PASS}/{TOTAL} tests passed.")

if __name__ == "__main__":
    run_all()
