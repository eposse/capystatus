import sys
import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_frame(is_success, failure_stage=0, step=0):
    b = '\\'
    
    # 1. MOVED BODY TEMPLATE (Two blank spacer rows added to the top to shift everything down)
    body_template = [
        "                                                              ", # Row 0: Top Padding
        "                                                              ", # Row 1: Top Padding
        "         _..---------------------------------------------.._  ", # Row 2 (Original Row 0)
        "       .'                                                   `-",
        "      /                                                       ",
        "     |                                                        ", 
        "     |                                                                                     ",
        "     |                                                        /                            ",
        "     |                                                       /                             ",
        "     |                                                      /                              ",
        "      \\                                                    /                               ",
        "       \\                                                  /                                ",
        "        `._                                            _.'                                 ",
        "           `''--...____________________________...--''`                                     ",
        "               ||   ||                   ||   ||                                            ",
        "               ||   ||                   ||   ||                                            ",
        "              (____)____)                 (____)____)                                       "
    ]

    if is_success:
        if (step // 4) % 2 == 1:
            body_template[14] = f"                {b}{b}   /                    {b}{b}   /                                               "
            body_template[15] = f"                 {b}{b} /                      {b}{b} /                                                "
            body_template[16] = "                (____)                    (____)                                              "

    grid = [list(row) for row in body_template]

    # 2. YOUR EXACT RECTANGULAR HEAD OVERLAY CONFIGURATION
    eye = "(O)" if is_success else "(X)"
    me = "\\" if is_success else "/"
    head_overlay = [
         "   ",                                   # Row 0: Ears
         " __ _________________________.",        # Row 1: Crown Line
         "(  )                   |     \\",        # Row 2: Brow Spacer Line
         "|   |                  | (O) |",        # Row 3: Brow/Snout Ridge
        f"|  {eye}                 \\_____/",        # Row 4: Eye Level
         "|   |                      |",          # Row 5: Jowl/Mouth Spacer Line
        f"|   |                    {me}-|",          # Row 6: Chin Depth Line
         "\\_________________________/ "           # Row 7: Jaw Base Boundary Line
    ]

    # 3. CONSOLE GRID BLITTING (Starts safely at row 0, perfectly aligned with the padded body)
    col_start = 62
    row_start = 0 if is_success else failure_stage

    for h_row_idx, head_line in enumerate(head_overlay):
        current_row = row_start + h_row_idx
        if 0 <= current_row < len(grid):
            head_chars = list(head_line)
            
            while len(grid[current_row]) < (col_start + len(head_chars)):
                grid[current_row].append('s')
                
            for char_idx, char in enumerate(head_chars):
                grid[current_row][col_start + char_idx] = char

    # 4. SERIALIZE MATRIX TO FINAL STRINGS
    title = "✅ YAY! \n" if is_success else "❌ OH NOOO! \n"
    flat_lines = ["".join(row) for row in grid]
    
    return title + "\n" + "\n".join(flat_lines)

def main():
    is_success = True
    if len(sys.argv) > 1 and (sys.argv[1] == "--fail" or sys.argv[1] == "-f"):
        is_success = False

    log_content = ""
    if os.path.exists("capy_output.log"):
        with open("capy_output.log", "r", encoding="utf-8") as f_in:
            log_content = f_in.read()

    if not is_success:
        timings = [0.9, 0.45, 0.45, 0.8]
        for stage, duration in enumerate(timings):
            clear_screen()
            print(render_frame(is_success=False, failure_stage=stage))
            time.sleep(duration)
        
        if log_content.strip():
            print("\n--- Execution Log (Error) ---")
            print(log_content)
    else:
        for step in range(0, 36, 4):
            padding = " " * step
            clear_screen()
            frame_text = render_frame(is_success=True, step=step)
            for line in frame_text.split('\n'):
                print(padding + line) if line.strip() else print(line)
            time.sleep(0.22)
            
        if log_content.strip():
            print("\n--- Execution Log (Standard Output) ---")
            print(log_content)

if __name__ == "__main__":
    main()
