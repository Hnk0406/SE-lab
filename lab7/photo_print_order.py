import math


def parse_order(text):
    """Parse 'size:copies' (e.g. '4x6:25') -> ('4X6', 25).

    Returns None for any invalid input (non-string, wrong number of ':'
    separators, empty size, non-integer or non-positive copies).
    """
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    size = parts[0].strip().upper()
    if not size:
        return None
    try:
        copies = int(parts[1].strip())
    except (ValueError, OverflowError):
        return None
    if copies <= 0:
        return None
    return size, copies


def file_size_average(sizes_csv):
    """Average of comma-separated non-negative integer file sizes (MB).

    Returns 0 for invalid input: non-string, empty string, empty or
    non-numeric elements, or negative sizes.
    """
    if not isinstance(sizes_csv, str):
        return 0
    values = []
    for item in sizes_csv.split(','):
        try:
            value = int(item.strip())
        except (ValueError, OverflowError):
            return 0
        if value < 0:
            return 0
        values.append(value)
    if not values:
        return 0
    return sum(values) // len(values)


def payable_amount(text):
    """Compute amount * 1.18 (18% tax) - discount from 'amount|discount'.

    Returns 0.0 for invalid input: non-string, wrong number of '|' separators,
    non-numeric, NaN/infinite or negative values. Result is never negative.
    """
    if not isinstance(text, str):
        return 0.0
    parts = text.split('|')
    if len(parts) != 2:
        return 0.0
    try:
        amount = float(parts[0].strip())
        discount = float(parts[1].strip())
    except (ValueError, OverflowError):
        return 0.0
    if not (math.isfinite(amount) and math.isfinite(discount)):
        return 0.0
    if amount < 0 or discount < 0:
        return 0.0
    total = amount * 1.18 - discount
    if not math.isfinite(total):
        return 0.0
    return max(total, 0.0)


def main():
    print("==== Running parse_order ====")
    user_input = input("Enter print size:copies (e.g. 4x6:25): ")
    result = parse_order(user_input)
    print("Size and Copies:", result)

    print("\n==== Running file_size_average ====")
    user_input = input("Enter file sizes in MB as CSV (e.g. 4,8,12): ")
    result = file_size_average(user_input)
    print("Average File Size:", result)

    print("\n==== Running payable_amount ====")
    user_input = input("Enter amount|discount (e.g. 450|50): ")
    result = payable_amount(user_input)
    print("Payable Amount:", result)


if __name__ == "__main__":
    main()