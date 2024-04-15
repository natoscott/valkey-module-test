#include "valkeymodule.h"
int TestCommand(ValkeyModuleCtx *ctx, ValkeyModuleString **argv, int argc) {

  return ValkeyModule_ReplyWithSimpleString(ctx, "OK");
}

int ErrCommand(ValkeyModuleCtx *ctx, ValkeyModuleString **argv, int argc) {
  return ValkeyModule_ReplyWithError(ctx, "ERR");
}

/* Registering the module */
int ValkeyModule_OnLoad(ValkeyModuleCtx *ctx, ValkeyModuleString **argv, int argc) {
  if (ValkeyModule_Init(ctx, "test", 1, VALKEYMODULE_APIVER_1) == VALKEYMODULE_ERR) {
    return VALKEYMODULE_ERR;
  }
  if (ValkeyModule_CreateCommand(ctx, "test.test", TestCommand, "readonly", 0,0,0) == VALKEYMODULE_ERR) {
    return VALKEYMODULE_ERR;
  }
  if (ValkeyModule_CreateCommand(ctx, "test.error", ErrCommand, "readonly", 0,0,0) == VALKEYMODULE_ERR) {
    return VALKEYMODULE_ERR;
  }
  return VALKEYMODULE_OK;
}
