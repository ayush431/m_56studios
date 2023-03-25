def performBatchOperation(table_obj, data_array, operation, fields=[]):
    BATCH_SIZE = 100
    # Split data array into batch and perform operations,
    # read about python batch looping
    for each_batch in range(0, len(data_array), BATCH_SIZE):
        data = data_array[each_batch: each_batch+BATCH_SIZE]
        if operation == 'create':
            table_obj.objects.bulk_create(data)
        elif operation == 'update':
            table_obj.objects.bulk_update(data, fields)