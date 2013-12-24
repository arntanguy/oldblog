Title: Using C++11 enum class to define bitfield flags 
Date: 2013-12-16 
Tags: programmation, C++, C++11, enum 
Summary: Creating bitfields can be useful to send several parameters to a function. However, it can be quite heavy to set up. This articles shows you an easy way to do it!
disqus_identifier: geenux-CPP-ENUM-CLASS-BITFIELD-FLAGS

C++11 introduced the notion of **enum class**, which extends the notion of enum
to make it closer to a struct. Using this new feature, it is quite easy to
achieve bitfield flags by overriding operators.
The following header contains all you need to set up a bitfield enum.
All it does is wrap the enum within a structure and override some bit
manipulation operators **&**, **|** and **~**. This allows you to manipulate
the bitfield very easyly.

    ::cpp
        #ifndef __ENUM_FLAGS_H__
        #define __ENUM_FLAGS_H__
        
        #include <type_traits>


        template<typename T> using Underlying = typename std::underlying_type<T>::type;
        template<typename T> constexpr Underlying<T> underlying(T t) { return Underlying<T>(t); }


        template<typename T> struct Flags {
            T t;
            constexpr Flags(T t): t(t) { }
            constexpr operator T() const { return t; }
            constexpr explicit operator bool() const { return underlying(t); }
        };


        #define ENUM_FLAGS(T) \
            enum class T;   \
            constexpr Flags<T> operator&(T l, T r) { return T(underlying(l) & underlying(r)); } \
            constexpr T operator|(T l, T r) { return T(underlying(l) | underlying(r)); } \
            constexpr T operator~(T c) { return T(~underlying(c)); }

        #endif


Here is an exemple showing how to use it. Notice the macro **ENUM_FLAGS(T)**
above? Well, this is all you'll need to make it work. The parameter **T** is
the name of your enum class. This macro will
automatically override operators for you enum, and thus turn it into a
bitfield.

    ::cpp
        #include <iostream>
        #include "enum_flags.h"
        
        ENUM_FLAGS(Type);
        enum class Type {
            TYPE1 = 1 << 0,
            TYPE2 = 1 << 1,
            TYPE3 = 1 << 2
        };
        
        class Test {
            public:
                Type type;
                Test(Type t) { type = t; if(type & Type::TYPE2); }
        };
        
        
        int main() {
            Test te(Type::TYPE2);
            constexpr Type testType = Type::TYPE1 | Type::TYPE2;
            if(testType & te.type) {
                std::cout << "Bit matches";
            }
        }

You might be wondering about the **1 << x** part. It is the same as saying
$2^x$, that is, setting the bit at the **x** position to 1.
        
