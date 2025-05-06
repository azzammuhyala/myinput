# Ini adalah ilustrasi kode input() / stdin di terminal.
# Kode ini hanya bekerja di Windows.

import sys
import msvcrt

def myinput(prompt=''):
    buffer = []     # buffer untuk menyimpan input
    insert = False  # mode insert atau mode penimpaan teks
    cursor_pos = 0  # posisi kursor

    # tulis perintah input
    sys.stdout.write(prompt)
    sys.stdout.flush()

    while True:
        # baca input dari terminal
        key = ord(msvcrt.getch())

        above = cursor_pos > 0
        below = cursor_pos < len(buffer)

        # KeyboardInterrupt (kombinasi Ctrl + C), kode: 3
        if key == 3:
            raise KeyboardInterrupt

        # backspace, kode: 8
        elif key == 8:
            # jika buffer tidak kosong
            if buffer:
                sys.stdout.write('\x1b[D')  # geser kursor ke kiri sebanyak 1 langkah
                sys.stdout.write('\x1b[P')  # hapus dan geser semua karakter ke kiri
                sys.stdout.flush()

                cursor_pos -= 1  # kurangi posisi kursor

                del buffer[cursor_pos]  # hapus karakter di buffer

        # enter, kode: 13
        elif key == 13:
            sys.stdout.write('\n')  # tambah karakter enter

            # jika menemui kode 26 (kombinasi Ctrl + Z) maka lempar EOFError (meniru fungsi input() di Python)
            if 26 in buffer:
                raise EOFError

            # kembalikan string buffer sebagai input
            return ''.join(map(chr, buffer))

        # kunci spesial
        elif key == 224:
            # baca kunci berikutnya (kunci spesialnya)
            key2 = ord(msvcrt.getch())

            # home, kode: 71
            if key2 == 71:
                # geser kursor ke awal
                sys.stdout.write('\x1b[')
                sys.stdout.write(str(cursor_pos))  # geser kursor ke kiri sebanyak cursor_pos
                sys.stdout.write('D')
                sys.stdout.flush()

                cursor_pos = 0

            # left, kode: 75
            elif key2 == 75:
                # jika posisi kursor di atas 0
                if above:
                    sys.stdout.write('\x1b[D')  # geser kursor ke kiri sebanyak 1 langkah
                    sys.stdout.flush()

                    cursor_pos -= 1

            # right, kode: 77
            elif key2 == 77:
                if below:
                    sys.stdout.write('\x1b[C')  # geser kursor ke kanan sebanyak 1 langkah
                    sys.stdout.flush()

                    cursor_pos += 1

            # end, code: 79
            elif key2 == 79:
                move = len(buffer) - cursor_pos

                # geser kursor ke akhir
                if move > 0:
                    sys.stdout.write('\x1b[')
                    sys.stdout.write(str(move))  # geser kursor ke kanan sebanyak move
                    sys.stdout.write('C')
                    sys.stdout.flush()

                cursor_pos = len(buffer)

            # insert, code: 82
            elif key2 == 82:
                insert = not insert

        # kunci lainnya (sebagai input)
        else:
            char = chr(key)  # ubah kode ASCII ke karakter

            # kondisi ketika mode insert (timpa)
            if insert and below:
                sys.stdout.write(char)

                buffer[cursor_pos] = key

            # kondisi ketika posisi kursor tidak di akhir
            elif below:
                sys.stdout.write('\x1b[@')  # geser semua karakter setelah kursor ke kanan
                sys.stdout.write(char)  # tulis karakter baru

                buffer.insert(cursor_pos, key)

            # kondisi ketika posisi kursor di akhir
            else:
                sys.stdout.write(char)

                buffer.append(key)

            sys.stdout.flush()

            cursor_pos += 1

if __name__ == '__main__':
    print(myinput())
