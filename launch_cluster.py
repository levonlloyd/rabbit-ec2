import boto
import sys
import gzip
import StringIO
import time

def launch_cluster(ami, number, user_data_script):
    """Launch a cluster of rabbit mq nodes on ec2"""
    ec2 = boto.connect_ec2()
    # launch master
    master_user_data = read_user_data(user_data_script)
    reservation = ec2.run_instances(ami, security_groups=['default'],
                      user_data=master_user_data, instance_type='m1.large',
                      placement=None)
    private_dns = wait_until_running(reservation)
    master_rabbit = make_master_name(private_dns)
    print master_rabbit
    # compute configuration for slaves
    # launch slaves
    num_slaves = number - 1
    if num_slaves > 0:
        reservation = ec2.run_instances(ami, security_groups=['default'],
                      user_data=master_user_data, instance_type='m1.large',
                      placement=None, min_count=num_slaves, max_count=num_slaves)

def make_master_name(private_dns):
    """Take an ec2 private dns and turn it into
       a rabbit name.
       NOTE: This assumes the rabbit name is
       rabbit@(PART OF DNS NAME BEFORE ."""
    return "rabbit@{0}".format(private_dns.partition('.')[0])

def wait_until_running(reservation):
    """Wait until the machine in the reservation is running.  
       When it is, return it's private dns name"""
    while True:
        status = reservation.instances[0].update()
        if status == 'running':
            return reservation.instances[0].private_dns_name
        else:
            print "Status is {0}".format(status)
            time.sleep(15)

def read_user_data(user_data_file):
    """Read a file and put it into a compressed byte string so it
       can be used a the user data string"""
    pass
    raw_string = ''
    with open(user_data_file, 'r') as f:
        raw_string = f.read()

    result = StringIO.StringIO()
    compressed = gzip.GzipFile(mode='wb',fileobj=result)
    compressed.write(raw_string)
    compressed.close()
    return result.getvalue()

if __name__ == '__main__':
    launch_cluster(sys.argv[1], int(sys.argv[2]), sys.argv[3])
