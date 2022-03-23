import sympy.ntheory as nt
import math
import json

#Verify that n has no prime power factor
def verify_no_prime_power_factors(exponents):
    for exponent in exponents:
        if exponent != 1:
            print("Exiting: n is not a composite of two primes.")
            quit()
    print("Continuing: Verified that n has no prime power factors, only prime factors.")

#Verify that n has exactly two prime factors
def verify_exactly_two_prime_factors(primes):
    if len(primes) != 2:
        print("Exiting: n does not have exactly two prime factors.")
        quit()
    print("Continuing: Verified that n has exactly two prime factors.")

#Solve linear congruence function.
#Source: https://stackoverflow.com/questions/48252234/how-to-solve-a-congruence-system-in-python
def linear_congruence(a, b, m):
    if b == 0:
        return 0

    if a < 0:
        a = -a
        b = -b

    b %= m
    while a > m:
        a -= m

    return (m * linear_congruence(m, -b, a) + b) // a

#Extract the digit for decoding
def extract_digits(message):
    digits = []
    while math.log10(message) > 2:
        digits.insert(0, message % 100)
        message = int((message - (message % 100))/100)
    if message != 0:
        digits.insert(0, message)
    return digits

#Decode a list of digits
def decode_digits(digits):
    decoded_message = ""
    with open("codebook.json") as file:
        codebook = json.load(file)
        values = list(codebook.values())
        keys = list(codebook.keys())
        for digit in digits:
            try:
                index = values.index(digit)
                decoded_message += str(keys[index])
            except Exception as e:
                print("Value mismatch, skipping character")
    return decoded_message

#Function executes on script execution
def main():
    #Public keys
    n = 3070475477
    e = 443

    #Allocate memory for recieved messages and for decrypted messages
    messages = [2360943706, 103447229, 416358637, 562123654, 308364848, 2892292118]

    #Factor the composite n to calculate p and q
    factors = nt.factorint(n)
    primes = list(factors.keys())
    exponents = list(factors.values())

    #Verify that n is a valid composite
    verify_no_prime_power_factors(exponents)
    verify_exactly_two_prime_factors(primes)

    #Print factors
    for factor in primes:
        print("Prime factor is: " + str(factor))

    #Calculate Euler's phi function of n
    print("Calculating Euler's phi function of n")
    phi_n = nt.totient(n)
    print("Phi of n is: " + str(phi_n))

    #Calculate f such that ef is congruent to 1 mod phi of n
    print("Calculating f such that ef is congruent to 1 mod phi of n")
    f = linear_congruence(e, 1, phi_n)
    print("Value of f is: " + str(f))

    #Decrypt each message by raising it to the power f
    digits = []
    print("Decrypting and decoding message")
    for message in messages:
        decrypted_message = pow(message, f, n)
        for digit in extract_digits(decrypted_message):
            digits.append(digit)
    print("Decrypted and decoded message is: " + decode_digits(digits))

#Execute main function
if __name__ == "__main__":
    main()