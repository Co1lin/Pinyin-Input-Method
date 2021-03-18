import argparse

input_file_path = ''
output_file_path = ''

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Pinyin Input Method',
        description='Pinyin to Chinese.',
        allow_abbrev=True,
    )

    parser.add_argument('-i', '--input-file', dest='input_file_path', type=str, default='input.txt', help="Input file", required=True)
    parser.add_argument('-o', '--output-file', dest='output_file_path', type=str, default='output.txt', help="Output file")

    # Load args
    args = parser.parse_args()
    input_file_path = args.input_file_path
    output_file_path = args.output_file_path

    # process the input
    with open(input_file_path) as input_file:
        with open(output_file_path, 'r') as output_file:

            while True:
                line = input_file.readline()
                if not line:
                    break

                output_file.write()
