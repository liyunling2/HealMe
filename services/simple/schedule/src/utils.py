def get_filtered_query_from_args(request_args, entity):

    def equality_filter_builder(arg_tuples_list, entity):
        if len(arg_tuples_list) == 0:
            return entity.query
        
        field, val = arg_tuples_list[0]
        remaining_args = arg_tuples_list[1: ]
        kwarg_dic_pair = {field: val}

        return equality_filter_builder(remaining_args, entity).filter_by(**kwarg_dic_pair)


    request_args_tuple_pairs = [(field, val) for field, val in request_args.items()]
    return equality_filter_builder(request_args_tuple_pairs, entity).all()