// Publish client

#include <stdlib.h>
#include <string.h>
#include "zmq.h"


int main (int argc, char const *argv[]) {
  
  void* context = zmq_ctx_new();
  //create a PUB socket
  void* publisher = zmq_socket(context, ZMQ_PUB);
  int conn = zmq_bind(publisher, "tcp://*:4040");
  conn = zmq_bind(publisher, "ipc://stock.ipc");
  
  const char* companies[3] = {"Company1", "Company10", "Company101"};

  for(;;) {
    int price = count % 17;
    int which_company = count % 3;
    int index = strlen(companies[which_company]);
    char update[64];
    sprintf(update, "%s| %d", companies[which_company], price);
    zmq_msg_t message;
    zmq_msg_init_size(&message, index);
    memcpy(zmq_msg_data(&message), update, index);
    zmq_msg_send(&message, publisher, 0);
    zmq_msg_close(&message);
    count++;
  }

  zmq_close(publisher);
  zmq_ctx_destroy(context);
  
  return 0;
}