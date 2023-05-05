// Bundle API auto-generated header file. Do not edit!
// Glow Tools version: 2022-05-11 (2ee55ec50) (Glow_Release_MCUX_SDK_2.12.0)

#ifndef _GLOW_BUNDLE_MODEL_H
#define _GLOW_BUNDLE_MODEL_H

#include <stdint.h>

// ---------------------------------------------------------------
//                       Common definitions
// ---------------------------------------------------------------
#ifndef _GLOW_BUNDLE_COMMON_DEFS
#define _GLOW_BUNDLE_COMMON_DEFS

// Glow bundle error code for correct execution.
#define GLOW_SUCCESS 0

// Memory alignment definition with given alignment size
// for static allocation of memory.
#define GLOW_MEM_ALIGN(size)  __attribute__((aligned(size)))

// Macro function to get the absolute address of a
// placeholder using the base address of the mutable
// weight buffer and placeholder offset definition.
#define GLOW_GET_ADDR(mutableBaseAddr, placeholderOff)  (((uint8_t*)(mutableBaseAddr)) + placeholderOff)

#endif

// ---------------------------------------------------------------
//                          Bundle API
// ---------------------------------------------------------------
// Model name: "model"
// Total data size: 41728 (bytes)
// Activations allocation efficiency: 1.0000
// Placeholders:
//
//   Name: "serving_default_input_1_0"
//   Type: i8[S:0.584702909 O:83][-123.372,25.727]<1 x 49 x 10 x 1>
//   Size: 490 (elements)
//   Size: 490 (bytes)
//   Offset: 0 (bytes)
//
//   Name: "StatefulPartitionedCall_0"
//   Type: i8[S:0.003906250 O:-128][0.000,0.996]<1 x 12>
//   Size: 12 (elements)
//   Size: 12 (bytes)
//   Offset: 512 (bytes)
//
// NOTE: Placeholders are allocated within the "mutableWeight"
// buffer and are identified using an offset relative to base.
// ---------------------------------------------------------------
#ifdef __cplusplus
extern "C" {
#endif

// Placeholder address offsets within mutable buffer (bytes).
#define MODEL_serving_default_input_1_0  0
#define MODEL_StatefulPartitionedCall_0  512

// Memory sizes (bytes).
#define MODEL_CONSTANT_MEM_SIZE     24448
#define MODEL_MUTABLE_MEM_SIZE      576
#define MODEL_ACTIVATIONS_MEM_SIZE  16704

// Memory alignment (bytes).
#define MODEL_MEM_ALIGN  64

// Bundle entry point (inference function). Returns 0
// for correct execution or some error code otherwise.
int model(uint8_t *constantWeight, uint8_t *mutableWeight, uint8_t *activations);

// -----------------------------------------------------------------------------
// Callback function used for Glow IR instruction instrumentation:
// - This callback is called by the bundle BEFORE executing each instruction.
// - This callback must be defined by the bundle user application.
// ARGUMENTS:
//   id     - Instruction instance ID.
//   kind   - Instruction kind (type).
//   opInp  - Number of input operands.
//   opOut  - Number of output operands.
//   opAddr - Array with addresses for all operands. The addresses are listed
//            first for the input operands and then for the output operands.
//            The array contains opInp + opOut addresses.
//   opSize - Array with sizes (in bytes) for all operands. The sizes are listed
//            first for the input operands and then for the output operands.
//            The array contains opInp + opOut sizes.
// NOTES:
// - This callback should be used to dump only the input operands since the
//   output operands are not yet computed/written when this callback is used.
// - This callback uses C linkage therefore if the callback is implemented in a
//   .cpp file you must enclose the implementation in extern "C" {}.
// - Look in the metafile "instrument-ir.info" generated during compile-time
//   to see more information about the instrumented instructions.
// -----------------------------------------------------------------------------
void glow_instrument_before(int id, int kind, int opInp, int opOut, uint8_t **opAddr, int *opSize);

// -----------------------------------------------------------------------------
// Callback function used for Glow IR instruction instrumentation:
// - This callback is called by the bundle AFTER executing each instruction.
// - This callback must be defined by the bundle user application.
// ARGUMENTS:
//   id     - Instruction instance ID.
//   kind   - Instruction kind (type).
//   opInp  - Number of input operands.
//   opOut  - Number of output operands.
//   opAddr - Array with addresses for all operands. The addresses are listed
//            first for the input operands and then for the output operands.
//            The array contains opInp + opOut addresses.
//   opSize - Array with sizes (in bytes) for all operands. The sizes are listed
//            first for the input operands and then for the output operands.
//            The array contains opInp + opOut sizes.
// NOTES:
// - This callback should be used to dump only the output operands since some
//   of the input operands might have been overwritten for instructions which
//   perform in-place computation.
// - This callback uses C linkage therefore if the callback is implemented in a
//   .cpp file you must enclose the implementation in extern "C" {}.
// - Look in the metafile "instrument-ir.info" generated during compile-time
//   to see more information about the instrumented instructions.
// -----------------------------------------------------------------------------
void glow_instrument_after(int id, int kind, int opInp, int opOut, uint8_t **opAddr, int *opSize);

#ifdef __cplusplus
}
#endif
#endif
