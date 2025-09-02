 def check_point_equality_3d(x1, y1, z1, x2, y2, z2):
    # Make all expansions the same length
    max_length = max(len(x1), len(y1), len(z1), len(x2), len(y2), len(z2))
    x1 = pad_with_zeros(x1, max_length)
    y1 = pad_with_zeros(y1, max_length)
    z1 = pad_with_zeros(z1, max_length)
    x2 = pad_with_zeros(x2, max_length)
    y2 = pad_with_zeros(y2, max_length)
    z2 = pad_with_zeros(z2, max_length)

    # Check equality
    is_equal = (x1 == x2) and (y1 == y2) and (z1 == z2)

    if is_equal:
        print("The points are equal")
    else:
        print("The points are not equal")

    return is_equal


def to_p_adic(n, p):
    if p <= 1:
        raise ValueError("Base p must be a prime number greater then 1.")

    if n == 0:
        return [0]

    digits = []

    while n != 0:
        digits.append(n % p)
        n //= p
    return digits


# ✅ FIXED: proper p-adic split mod p²
def to_split_coords(n, p=5):
    """
    Convert integer n into (a0, a1) such that
    n ≡ a0 + a1·p (mod p²), with 0 <= a0,a1 < p
    """
    n_mod = n % (p**2)
    a0 = n_mod % p
    a1 = n_mod // p   # <-- FIXED: removed "% p"
    return (a0, a1)


def pad_with_zeros(arr, length):
    return arr + [0] * (length - len(arr))


def main():
    print("Calculation of point addition on curve y^2z=x^3 + Axz^2 + Bz^3")
    x1 = [int(x) for x in input("Enter the x1 p-adic expansion (comma-separated): ").split(',')]
    y1 = [int(x) for x in input("Enter the y1 p-adic expansion (comma-separated): ").split(',')]
    z1 = [int(x) for x in input("Enter the z1 p-adic expansion (comma-separated): ").split(',')]
    x2 = [int(x) for x in input("Enter the x2 p-adic expansion (comma-separated): ").split(',')]
    y2 = [int(x) for x in input("Enter the y2 p-adic expansion (comma-separated): ").split(',')]
    z2 = [int(x) for x in input("Enter the z2 p-adic expansion (comma-separated): ").split(',')]
    p = int(input("Enter the base (prime number): "))
    A = int(input("Enter the value of A: "))
    B = int(input("Enter the value of B: "))

    try:
        # First print intermediate values for debugging
        print(f"\nInput values:")
        print(f"P1: x={x1}, y={y1}, z={z1}")
        print(f"P2: x={x2}, y={y2}, z={z2}")
        print(f"Parameters: p={p}, A={A}, B={B}")

        X10 = x1[0]
        Y10 = y1[0]
        Z10 = z1[0]

        X20 = x2[0]
        Y20 = y2[0]
        Z20 = z2[0]

        X11 = x1[1]
        Y11 = y1[1]
        Z11 = z1[1]

        X21 = x2[1]
        Y21 = y2[1]
        Z21 = z2[1]

        # Check equality and perform appropriate operation
        if check_point_equality_3d(x1, y1, z1, x2, y2, z2):
            print("P1 == P2, using doubling formula")

            X3 = (2 * Y10 * Z10 * (3 * X10**2 + A * Z10**2)**2 + 16 * (p - 1) * X10 * Y10**3 * Z10**2) + (
                4 * Y10 * Z10 * (3 * X10**2 + A * Z10**2) * (6 * X10 * X11 + 2 * A * Z10 * Z11)
                + 16 * (p - 1) * (X10 * Y10**2 * Z10 + X10 * Y10**2 * Z11 + 2 * X10 * Y10 * Y11 * Z10 + X11 * Y10**2 * Z10) * Y10 * Z10
                + 2 * (Y10 * Z11 + Y11 * Z10) * ((3 * X10**2 + A * Z10**2)**2 + 8 * (p - 1) * X10 * Y10**2 * Z10)) * p

            Y3 = ((3 * X10**2 + A * Z10**2) * (12 * X10 * Y10**2 * Z10 + (p - 1) * (3 * X10**2 + A * Z10**2)**2)
                  + 8 * (p - 1) * Y10**4 * Z10**2) + (
                (3 * X10**2 + A * Z10**2) * (12 * X10 * Y10**2 * Z11 + 24 * X10 * Y10 * Y11 * Z10
                + 12 * X11 * Y10**2 * Z10) + (3 * X10**2 + A * Z10**2)**2 * (p - 1) * (12 * X10 * X11 + 4 * A * Z10 * Z11)
                + (p - 1) * (3 * X10**2 + A * Z10**2)**3 + 8 * (p - 1) * (Y10**4 * Z10**2 + 4 * Y10**3 * Y11 * Z10**2 + 2 * Y10**4 * Z10 * Z11)
                + (6 * X10 * X11 + 2 * A * Z10 * Z11) * (12 * X10 * Y10**2 * Z10 + (p - 1) * (3 * X10**2 + A * Z10**2)**2)) * p

            Z3 = (8 * Y10**3 * Z10**3) + (8 * 3 * Y10**2 * Y11 * Z10**3 + 8 * 3 * Y10**3 * Z10**2 * Z11) * p
            print(X3, Y3, Z3)
        else:
            print("P1 != P2, computing P1 + P2")

            X3 = (Z10 * Z20 * (X20 * Z10 + (p - 1) * X10 * Z20) * (Y20 * Z10 + (p - 1) * Y10 * Z20)**2 + (p - 1) * (X20 * Z10 + (p - 1) * X10 * Z20)**4 + 2 * (p - 1) * (X20 * Z10 + (p - 1) * X10 * Z20)**3 * X10 * Z20) \
                + (2 * (X20 * Z10 + (p - 1) * X10 * Z20) * (Y21 * Z10 + Y20 * Z11 + (p - 1) * (Y10 * Z20 + Y10 * Z21 + Y11 * Z20)) * Z10 * Z20 * (Y20 * Z10 + (p - 1) * Y10 * Z20)
                + (Y20 * Z10 + (p - 1) * Y10 * Z20)**2 * (X21 * Z10 + X20 * Z11 + (p - 1) * (X10 * Z20 + X10 * Z21 + X11 * Z20)) * Z10 * Z20 + (Z11 * Z20 + Z10 * Z21) * (Y20 * Z10 + (p - 1) * Y10 * Z20)**2 * (X20 * Z10 + (p - 1) * X10 * Z20)
                + 4 * (p - 1) * (X20 * Z10 + (p - 1) * X10 * Z20)**3 * (X21 * Z10 + X20 * Z11 + (p - 1) * (X10 * Z20 + X10 * Z21 + X11 * Z20)) + (p - 1) * (X20 * Z10 + (p - 1) * X10 * Z20)**4
                + 6 * (p - 1) * (X20 * Z10 + (p - 1) * X10 * Z20)**2 * (X21 * Z10 + X20 * Z11 + (p - 1) * (X10 * Z20 + X10 * Z21 + X11 * Z20)) * X10 * Z20
                + 2 * (p - 1) * (X20 * Z10 + (p - 1) * X10 * Z20)**3 * (X11 * Z20 + X10 * Z21) + 2 * (p - 1) * (X20 * Z10 + (p - 1) * X10 * Z20)**3 * X10 * Z20) * p

            Y3 = ((X20 * Z10 + (p - 1) * X10 * Z20)**2 * (3 * X10 * Z20 * (Y20 * Z10 + (p - 1) * Y10 * Z20) + (X20 * Z10 + (p - 1) * X10 * Z20) * (Y20 * Z10 + 2 * (p - 1) * Y10 * Z20))
                  + (p - 1) * Z10 * Z20 * (Y20 * Z10 + (p - 1) * Y10 * Z20)**3) + ((X20 * Z10 + (p - 1) * X10 * Z20)**2 * (3 * (X10 * Z21 + X11 * Z20) * (Y20 * Z10 + (p - 1) * Y10 * Z20)
                  + 3 * X10 * Z20 * (Y21 * Z10 + Y20 * Z11 + (p - 1) * (Y10 * Z20 + Y10 * Z21 + Y11 * Z20)) + (X20 * Z10 + (p - 1) * X10 * Z20) * (Y21 * Z10 + Y20 * Z11 + 2 * (p - 1) * (Y10 * Z20 + Y10 * Z21 + Y11 * Z20))
                  + (X21 * Z10 + X20 * Z11 + (p - 1) * (X10 * Z20 + X10 * Z21 + X11 * Z20)) * (Y20 * Z10 + 2 * (p - 1) * Y10 * Z20)) + (p - 1) * (Y20 * Z10 + (p - 1) * Y10 * Z20)**3 * (Z11 * Z20 + Z10 * Z21)
                  + 3 * (p - 1) * Z10 * Z20 * (Y20 * Z10 + (p - 1) * Y10 * Z20)**2 * (Y21 * Z10 + Y20 * Z11 + (p - 1) * (Y10 * Z20 + Y10 * Z21 + Y11 * Z20)) + (p - 1) * Z10 * Z20 * (Y20 * Z10 + (p - 1) * Y10 * Z20)**3
                  + 2 * (X20 * Z10 + (p - 1) * X10 * Z20) * (X21 * Z10 + X20 * Z11 + (p - 1) * (X10 * Z20 + X10 * Z21 + X11 * Z20)) * (3 * X10 * Z20 * (Y20 * Z10 + (p - 1) * Y10 * Z20)
                  + (X20 * Z10 + (p - 1) * X10 * Z20) * (Y20 * Z10 + 2 * (p - 1) * Y10 * Z20))) * p

            Z3 = (Z10 * Z20 * (X20 * Z10 + (p - 1) * X10 * Z20)**3) + (3 * Z10 * Z20 * (X20 * Z10 + (p - 1) * X10 * Z20)**2 * (X20 * Z11 + X21 * Z10 + (p - 1) * (X10 * Z20 + X10 * Z21 + X11 * Z20))
                 + (Z11 * Z20 + Z10 * Z21) * (X20 * Z10 + (p - 1) * X10 * Z20)**3) * p
            print(X3, Y3, Z3)

        result_x = to_split_coords(X3, p)
        result_y = to_split_coords(Y3, p)
        result_z = to_split_coords(Z3, p)

        # Format result to_split_coords better clarity
        print("\nFinal result in p-adic form:")
        print(f"X = {result_x[0]} + {result_x[1]}·{p} + O({p}²)")
        print(f"Y = {result_y[0]} + {result_y[1]}·{p} + O({p}²)")
        print(f"Z = {result_z[0]} + {result_z[1]}·{p} + O({p}²)")
    except Exception as e:
        print(f"Error occurred during calculation: {e}")


# Execute the main function
if __name__ == "__main__":
    main()
