
class FilterValidator:
    @staticmethod
    def validate_filters(params: , filter_class) -> tuple[bool, list[str]]:
        """
        Validates that all query parameters are valid filter fields for the given filter class.

        Args:
            params (): Dictionary of query parameters to validate
            filter_class: Class containing valid filter fields (should have fields as class attributes)

        Returns:
            tuple[bool, list[str]]: A tuple containing:
                - bool: True if all filters are valid, False otherwise
                - list[str]: List of invalid filter names (empty if all are valid)
        """
        valid_filters = [field.lower() for field in vars(filter_class).keys()
                         if not field.startswith('_')]

        invalid_filters = [param for param in params.keys()
                           if param.lower() not in valid_filters]

        return (len(invalid_filters) == 0, invalid_filters)
