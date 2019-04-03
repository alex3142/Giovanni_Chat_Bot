import logging as log
log.basicConfig(level=log.INFO)

from giovanni.pipeline import Pipeline


def process_files(pipeline, files):

    for file_path in files:
        try:
            print("Processing file %s" % file_path)

            result = None
            with open(file_path, 'rb') as fd:
                if file_path.endswith('.wav'):
                    result = pipeline.process_audio(fd)

                elif file_path.endswith('.txt'):
                    result = pipeline.process_text(fd.read())

                else:
                    raise Exception("Unsupported file extension! (%s)" % file_path.rsplit(',')[-1])

            if result:
                print(result)
            else:
                print("The result is empty or None.")

        except Exception as e:
            print("Error! %s" % e)


def main(arguments):

    log.info("Loading the pipeline...")
    pipeline = Pipeline("resources/project_giovanni.0.1.ttl")
    log.info("Ready!")

    if arguments.files:
        process_files(pipeline, arguments.files)

    elif arguments.text:
        print("Processing text %s" % arguments.text)
        print(pipeline.process_text(arguments.text))

    else:
        print("\n")

        finish = False
        iteration_count = 0
        while not finish:

            # get input from user
            user_input = input("User: ")

            # add user input to the state
            response = pipeline.process_text(user_input)
            print("Giovanni: ", response)

            finish = pipeline.is_finished()

            iteration_count += 1
            if iteration_count > 20:
                print("Time's up! Bye.")
                finish = True
        print("\n")


if __name__ == "__main__":
    import argparse

    description = """Runs an interactive dialog agent.
It can run in batch mode, generating responses by processing audio (.wav) and text (.txt) files or plain text input."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('files', metavar='FILE', nargs='*',
                        help='file to be processed')
    parser.add_argument('-t', '--text', nargs='?',
                        help='plain text input to be processed')

    args = parser.parse_args()
    main(args)
