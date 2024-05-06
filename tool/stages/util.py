def sort_dict(data: dict):
    """
    Sort dictionary including children
    """
    def get_key(item):
        return f"{len(item)}{item}"

    if isinstance(data, dict):
        return {key: sort_dict(data[key]) for key in sorted(data, key=get_key)}
    else:
        return data


def encode_filename(category: str, filename: str, quality: str, format: str):
    """
    Encodes compressed file details to filename

    Output format:
        "category_-_filename_-_quality.format"
    """
    return f"{category}_-_{filename}_-_{quality}.{format}"


def decode_file_details(encoded_filename: str) -> (str, str, str, str):
    """
    Decodes file details from compressed filename

    Input format:
        "category_-_filename_-_quality.format"

    Outputs:
        (catergory, filename, quality, format)
    """

    tmp = encoded_filename.split(".")
    filename_array = ''.join(tmp[:-1]).split("_-_")

    category = filename_array[0]
    filename = filename_array[1]
    quality = filename_array[2]
    format = tmp[-1]

    return (category, filename, quality, format)
