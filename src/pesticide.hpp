#pragma once
/**
 * PESTICIDE
 *
 * a small debugging library for C++
 * by qRea/WF, 2025
 *
 * For those who refuse to use a debugger!
 *
 * Made primarily for personal use, could be used by anyone who also finds it
 * useful. It's basic and jank but it does the job for me.
 */
#define PESTICIDE_ENABLED       // comment this if you want to disable this lib




#ifdef PESTICIDE_ENABLED

// necessary includes
#include <iostream> // IWYU pragma: keep (used by macros)
#include <chrono>   // IWYU pragma: keep (used by macros)
// #include <stacktrace>


// internal definitions
#define PESTICIDE_DEBUG_MSG     "DEBUG: "

#define PESTICIDE_PRINT_START   std::cout << PESTICIDE_DEBUG_MSG <<
#define PESTICIDE_PRINT_END     << std::endl


// external functions
#define pesticide_print(x)          PESTICIDE_PRINT_START x PESTICIDE_PRINT_END

#define pesticide_function          __FUNCTION__
// #define pesticide_stack             std::stacktrace::current()

#define pesticide_timer_start(x)    auto x##_start{std::chrono::high_resolution_clock::now()}
#define pesticide_timer_end(x)      auto x##_end{std::chrono::high_resolution_clock::now()}
#define pesticide_timer_print(x)    PESTICIDE_PRINT_START "Timer " #x ": " \
                                    << std::chrono::duration_cast<std::chrono::microseconds>(x##_end - x##_start).count() \
                                    << " microseconds" PESTICIDE_PRINT_END
#define pesticide_timer_endprint(x) pesticide_timer_end(x); pesticide_timer_print(x)


#endif
