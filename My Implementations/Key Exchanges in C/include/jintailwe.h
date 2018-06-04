/********************************************************************************************
 * A simple provably secure key exchange based on the learning with errors problem
 *
 *
 * Based on the paper:
 *     Jintai Ding, Xiang Xie and Xiaodong Ling
 *
 * Copyright (c) Jintai Ding, Xiang Xie and Xiaodong Ling for the theoretical key exchange
 *               Afraz Arif Khan for implementing the key exchange in C and TLS
 *
 * Released under the MIT License; see LICENSE.txt for details.
 ********************************************************************************************/

/** \file jintailwe.h
 * Core parameters and function prototypes for the PQC implementation
 */

#include <stdbool.h>

#ifndef HEADER_JINTAILWE_H

#define LATTICE_DIMENSION 512 // Matrix Dimension
#define MODULO_Q 2147483647 // q - The modulo factor

struct vector_params{
  int *secret_vector;
  int *public_vector;
};

struct matrix_params{
  int **secret_matrix;
  int **public_matrix;
};

/*-----------------------------Global Variables-------------------------------*/
int M[LATTICE_DIMENSION][LATTICE_DIMENSION]; //Public parameter M
int M_TRANSPOSE[LATTICE_DIMENSION][LATTICE_DIMENSION]; //M transpose
struct matrix_params Alice_params;
struct vector_params Alice1_params;
struct vector_params Bob_params;

//Alice Params
int **EA; //Alices Error Matrix
int *edashA; //Alices other error vector
int *KA;
int *SKA;

//----Resampling----
int *eA; // in case of resampling
int edashA_single; //for single bit value of KA

//Bob Params
int *eB; //Bobs Error vector
int *edashB; //Bobs Error Scalar
int *KB;
int *SKB;

//----Resampling----
int edashB_single; //for single bit value of KB

//Signal generated
int *sig; //either 0 or 1 at any index

/*------------------------------Function Prototypes---------------------------*/
extern void run_key_exchange(); //Running the key exchange protocol based on public params

extern void generate_gaussian_matrix(); // Generate a matrix sampled from the Discrete Gaussian distribution

extern void generate_gaussian_vector(int gauss_vec[LATTICE_DIMENSION]); // Generate a vector sampled from the Discrete Gaussian distribution

extern int generate_gaussian_scalar(); // Generate a discrete gaussian scalar value

extern int robust_extractor(int x, int sigma); // Find the same shared key

extern bool check_robust_extractor(int x, int y); // Condition for the validity of the robust extractor

extern int signal_function(int y, int b); // A hint algorithm

extern void generate_public_vector(int* secret_vec, int*error_vec, int* public_vec, bool client); //Single Vector Public in case of resampling

//----- Printing functions-----
extern void pretty_print_vector(int vec[LATTICE_DIMENSION]); //Prints a vector
extern void pretty_print_matrix(int **matrix); //Prints a matrix
//------------------ Public Parameters for the key Exchange -------------------
extern void generate_M();


//------------------ Generate gaussian numbers in C ----------------------------
extern inline long discrete_normal_distribution();

/*---------------------------End of Function Prototypes-----------------------*/

#endif
