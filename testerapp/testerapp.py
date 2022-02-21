import os
import re
import sys
import typing as tp
from pydantic import BaseModel, constr, validator


class InputArgs(BaseModel):
    arg : constr(regex=r'^TestInput[0-9][0-9].txt$')

class InputByte(BaseModel):
    byte_str: str

    @validator('byte_str')
    def byte_hex_match(cls, v):
        pat = re.compile(r'^[0-9a-fA-F][0-9a-fA-F]$')
        if not re.fullmatch(pat, v):
            arg = InputArgs(arg=sys.argv[1])
            out_file = 'TestOutput' + arg.arg[-6:-4] + '.txt'
            file_writer(out_file, 'w', 'FFFFFFFF')
            raise ValueError('not valid hex value')
        return v

def file_writer(filen: str, mode: str, output: str) -> None:
    with open(filen, mode) as fp:
        fp.writelines(output.upper())

def file_read(filen: str, mode) -> None:
    with open(filen, mode) as fp:
        file_content = fp.readlines()
        return file_content

def main():
    # Check if input file is given
    if len(sys.argv) != 2:
        print('You have to provide filename as argument')
        exit(1)
    arg = InputArgs(arg=sys.argv[1])

    file_content = file_read(arg.arg, 'r')
    out_file = 'TestOutput' + arg.arg[-6:-4] + '.txt'
    # delete ouput file if exists
    if os.path.isfile(out_file):
        os.remove(out_file)
   
    file_content = str(file_content[0]).strip('\n')
    file_length = len(file_content)
    start_indx = 0
    end_indx = 8
    output = ''

    while True:
        # Check if enough bytes to read
        if end_indx > file_length:
            output += 'FFFFEEEE'
            file_writer(out_file, 'a', output)
            return output

        # Convert 4 input bytes to hex string
        it = iter(file_content[start_indx:end_indx])
        hex_word = []
        for x in it:
            byte_str = InputByte(byte_str = x + next(it))
            hex_word.append(byte_str)
        hex_value_1 = hex_word[0].byte_str
        hex_value_2 = hex_word[1].byte_str
        hex_value = hex_value_1 + hex_value_2

        # Check if input value is greater then 256
        if int(hex_value,16) > 256:
            output += 'FFFF0100'
            # Check if end of file
            if end_indx == len(file_content):
                output += 'FFFF0000'
                file_writer(out_file, 'a', output)
                return output
            start_indx = end_indx
            end_indx *= 2
            continue

        hex_factor = hex_word[2].byte_str
        # Check if factor is between 0 and 255
        if int(hex_factor, 16) < 0 or int(hex_factor,16) > 254:
            output += 'FFFFFF00'
            # Check if end of file
            if end_indx == len(file_content):
                output += 'FFFF0000'
                file_writer(out_file, 'a', output)
                return output
            start_indx = end_indx
            end_indx *= 2
            continue

        hex_offset = hex_word[3].byte_str

        output_value = (int(hex_value, 16) * int(hex_factor, 16)) + int(hex_offset, 16)
        
        hex_output = hex(output_value)[2:]
        # Convert hex_output to 2 bytes
        if len(hex_output) == 1:
            output = output + '000' + hex_output
        else:
            output = output + '0' + hex_output[0] + hex_output[1:]

        # Check if end of file
        if end_indx == len(file_content):
            output += 'FFFF0000'
            file_writer(out_file, 'a', output)
            break 
        start_indx = end_indx
        end_indx *= 2
    return output

if __name__ == '__main__':
    main()


