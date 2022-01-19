from CodeWriter import Writer


def main():
    writer = Writer()
    with writer.block('static void main(String.. args) {', '}'):
        writer.print("System.out.println('Hello World');")
        with writer.block(r'int f() {', '}'):
            writer.print('int x = 1;', 'int y = 1;', sep='\n')
            with writer.listing('switch(x) {', 'case', '}'):
                writer.item('0: Do Something;')
                with writer.block(r'for {int i = 0; i < y; i++} {', '}'):
                    writer.print('y--;')
                writer.print('break;')
                writer.item('1: Something else;')
            writer.print('return x * y;')
        writer.print('exit();')


if __name__ == '__main__':
    main()
