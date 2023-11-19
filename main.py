def list_vpcs_and_subnets(request):
    """
    Responds to an HTTP request with a simple 'Hello World' message.
    """

    request_json = request.get_json(silent=True)
    # request_args = request.args # GET args 

    return request_json
