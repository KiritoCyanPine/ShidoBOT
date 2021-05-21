string = "15.jpg?token=02adcf12bc3951bd88176ff781cdca5defa89a96&ttl=1619798400"

a = string.index(".jpg")
print(string[:a+4])
