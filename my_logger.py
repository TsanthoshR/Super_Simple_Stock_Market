"""Logger configuration for the GBCE Stock Market application.

This module sets up daily and monthly loggers to capture application events
"""

import logging

from src.func_libs.take_date import TakeDate

today = TakeDate().now.strftime("%Y-%m-%d")

# current month
month = TakeDate().now.strftime("%B")

# create loggers
daily_logger = logging.getLogger("daily_logger")
monthly_logger = logging.getLogger("monthly_logger")


# set levels
daily_logger.setLevel(logging.DEBUG)
monthly_logger.setLevel(logging.DEBUG)

# Create handlers
stream_daily_handler = logging.StreamHandler()
file_daily_handler = logging.FileHandler(f"logs/daily_log_{today}.log")
file_monthly_handler = logging.FileHandler(f"logs/monthly_log_{month}.log")
# email_handler = logging.handlers.SMTPHandler(
#     mailhost=("smtp.example.com", 587),
#     fromaddr="santhosht529@gmail.com",
#     toaddrs=["example@noreply.com"],
#     subject="GBCE Log Report",
# )

# set levels for handlers
stream_daily_handler.setLevel(logging.INFO)
file_daily_handler.setLevel(logging.DEBUG)
file_monthly_handler.setLevel(logging.DEBUG)
# email_handler.setLevel(logging.ERROR)

# Create formatters
my_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)-8s -[%(pathname)s :: %(module)s \
  :: %(funcName)s : %(lineno)d ] - %(message)s",
    "%Y-%m-%d:%H:%M:%S",
)


# Add formatters to handlers
stream_daily_handler.setFormatter(my_format)
file_daily_handler.setFormatter(my_format)
file_monthly_handler.setFormatter(my_format)
# email_handler.setFormatter(my_format)

# Add handlers to loggers
daily_logger.addHandler(stream_daily_handler)
daily_logger.addHandler(file_daily_handler)
monthly_logger.addHandler(file_monthly_handler)
# daily_logger.addHandler(email_handler)


if __name__ == "__main__":
    pass
