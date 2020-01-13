def build_influx_tcp_structure(measurement: str, epoch: str = "default", value: float = 1.0, tags: dict = {}, fields: dict = {}) -> dict:
    """
    Builds data structure for Influx. To be used in the TCP port localhost:8086.\n
    This port is the InfluxDB Docker container running.
    If no epoch is passed, defaults to datetime.now().\n
    Expects:\n
        - measurement: Main value to search in Grafana. (similar to Table name)
        - value: The value of said measurement. Defaults to float 1. Unless the measurement is really simple with no relation to "fields", leave it at default.
        - epoch: Timestamp of the measurement. Format is 2019-03-20T00:08:44
        - fields: Optional: Dict if more fields want to be stored. Fields can contain values, like cpu usage, temperature, or traffic. Usually used with numeric values for plot.
        - tags: Optional: Dict with tags for this measurement. Tags can be used as identifiers or labels. Usually strings to sort data by groups.
    """
    try:
        # Nests dicts, first prepare all the things needed to form the structure
        # Check if epoch was provided and if is valid
        if epoch == "default":
            epoch = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
        else:
            # Test if it can be parsed to datetime
            try:
                # Add .0 in case that the epoch didn't include it
                if "." not in epoch:
                    epoch = epoch + ".0"
                datetime.datetime.strptime(epoch, '%Y-%m-%dT%H:%M:%S.%f')
            except Exception as exc:
                raise ValueError(f"Exception while building influx tcp structure, transforming the epoch passed into datetime: {exc}.\nUse format: 2019-03-20T00:08:44.883722\n")
        # value goes into fields, more like a placeholder
        fields["value"] = float(value)
        # Main dictionary
        data = {
            "measurement" : measurement,
            "time" : epoch,
        }
        # Nest dictionaries
        data["tags"] = tags
        data["fields"] = fields
        #print(data) # Debug
        return data
    except Exception as exc:
        raise ValueError(f"Exception while building influx tcp structure: {exc}.")