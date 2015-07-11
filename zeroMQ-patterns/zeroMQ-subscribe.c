// Subscribe client


#include <stdlib.h>
#include <string.h>
#include "zmq.h"


int main (int argc, char const *argv[]) {

  void* context = zmq_ctx_new();
  //create a SUB socket
  void* subscriber = zmq_socket(context, ZMQ_SUB);

  const char* filter;
  
  if(argc > 1) {
    filter = argv[1];
  } else {
    filter = "Company1|";
  }
  printf("Collecting stock information from the server.\n");

  int conn = zmq_connect(subscriber, "tcp://localhost:4040");
  // must set a subscription for SUB socket
  conn = zmq_setsockopt(subscriber, ZMQ_SUBSCRIBE, filter, strlen(filter));

  int i = 0;
  for(i = 0; i < 10; i++) {
    zmq_msg_t reply;
    zmq_msg_init(&reply);
    // receive the message, previous message is deallocated
    zmq_msg_recv(&reply, subscriber, 0);
    
    int length = zmq_msg_size(&reply);
    char* value = malloc(length + 1);
    memcpy(value, zmq_msg_data(&reply), length);
    zmq_msg_close(&reply);
    printf("%s\n", value);    
    free(value);

  }
  zmq_close(subscriber);
  zmq_ctx_destroy(context);

  return 0;
}