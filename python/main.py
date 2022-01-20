import bot
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", dest="is_training", action="store_true", default=False)
    parser.add_argument("command")
    parser.add_argument("api_key")

    args = parser.parse_args(sys.argv)

    if args.is_training:
        bot.train_model("EN")
    else:
        if args.api_key:
            bot.run(args.api_key)


