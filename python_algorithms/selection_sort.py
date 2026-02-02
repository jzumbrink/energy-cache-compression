def selection_sort(a: list[int]) -> None:
    for i in range(len(a) - 1):
        smallest: None | int = None
        smallest_index: None | int = None
        for j in range(i, len(a)):
            if smallest is None or smallest > a[j]:
                smallest = a[j]
                smallest_index = j
        old_i = a[i]
        a[i] = a[smallest_index]
        a[smallest_index] = old_i

if __name__ == "__main__":
    x = [8, 5, 7, 1, 9, 3]
    selection_sort(x)
    print(x)
