#!/usr/bin/env python

#
# Proto - Hop Labs task
# https://www.hoplabs.com/proto
#


import struct

# Constants and variables
transaction_file = 'files/txnlog.dat'
total_amount_debits = 0
total_amount_credits = 0
number_autopays_started = 0
number_autopays_ended = 0
marked_user = 2456938384156277127
marked_user_credit = 0
marked_user_debit = 0

# Function to get record type from enum value
def get_record_type(byte):
    switcher = {
        0: 'Debit',
        1: 'Credit',
        2: 'StartAutopay',
        3: 'EndAutopay'
    }
    return switcher.get(byte, None)

# header: 
# | 4 byte magic string "MPS7" | 1 byte version | 4 byte (uint32) # of records |

# Read binary file and skip first 9 bytes
f = open(transaction_file, 'rb')

# Get header information as a tuple
header = (f.read(4), f.read(1), int.from_bytes(f.read(4), byteorder='big'))
# We do nothing with the header

# Get all the records
while (byte := f.read(1)):
    # The first byte will be the record type enum
    record_type = get_record_type(int.from_bytes(byte, byteorder='big'))
    # Next 4 bytes will be the Unix timestamp
    timestamp = int.from_bytes(f.read(4), byteorder='big')
    # Next 8 bytes will be user ID
    userid = int.from_bytes(f.read(8), byteorder='big')
    # For Debit and Credit record types, there is an additional 8-byte field
    amount = None
    if record_type in ['Debit', 'Credit']:
        amount = struct.unpack('d', f.read(8))[0]
    print(record_type, timestamp, userid, amount)

    # If user is the marked user with ID 2456938384156277127
    if userid == marked_user:
        if record_type == 'Debit':
            marked_user_debit = amount
        elif record_type == 'Credit':
            marked_user_credit = amount

    # Increment
    if record_type == 'Debit':
        total_amount_debits += amount
    elif record_type == 'Credit':
        total_amount_credits += amount
    elif record_type == 'StartAutopay':
        number_autopays_started += 1
    elif record_type == 'EndAutopay':
        number_autopays_ended += 1

# Display information
print('-' * 80)
print("total credit amount={:.2f} \n\
total debit amount={:.2f} \n\
autopays started={} \n\
autopays ended={} \n\
balance for user {}={}" \
.format(total_amount_credits, total_amount_debits, number_autopays_started, \
        number_autopays_ended, marked_user, marked_user_credit - marked_user_debit))
print('*' * 80)

# Close the file
f.close()
