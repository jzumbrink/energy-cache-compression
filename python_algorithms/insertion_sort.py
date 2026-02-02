def insertion_sort(a: list[int]) -> None:
    for i in range(1, len(a)):
        reference_value: int = a[i]
        j = i
        while j > 0 and a[j-1] > reference_value:
            a[j] = a[j-1]
            j -= 1
        a[j] = reference_value

if __name__ == "__main__":
    x = [8, 5, 7, 1, 9, 3]
    insertion_sort(x)
    print(x)
