import { Suspense } from 'react'
import Image from 'next/image'
import HomeProductsBySubcategory from './components/HomeProductsBySubcategory'

function ProductsFallback() {
  return (
    <div className="space-y-16">
      {[...Array(3)].map((_, idx) => (
        <div key={idx} className="space-y-6">
          <div className="h-12 bg-gray-200 animate-pulse rounded"></div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-96 bg-gray-200 animate-pulse rounded-lg"></div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <header className="bg-white shadow-lg border-b-2 border-gold sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-6">
            <div className="flex items-center space-x-6">
              <Image
                src="/logo.svg"
                alt="HIGH GRADE DIAMONDS"
                width={280}
                height={168}
                className="h-24 w-auto"
                priority
              />
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h1 className="text-6xl font-serif text-charcoal mb-6 tracking-tight">
            Exquisite Diamond Collections
          </h1>
          <p className="text-xl text-gray-600 font-sans max-w-2xl mx-auto leading-relaxed">
            Discover our curated selection of high-grade diamonds, meticulously crafted into timeless pieces of elegance and sophistication.
          </p>
          <div className="mt-8 flex justify-center">
            <div className="w-24 h-1 bg-gold"></div>
          </div>
        </div>

        <Suspense fallback={<ProductsFallback />}>
          <HomeProductsBySubcategory />
        </Suspense>
      </main>

      <footer className="bg-charcoal text-white mt-20 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <Image
              src="/logo.svg"
              alt="HIGH GRADE DIAMONDS"
              width={280}
              height={168}
              className="h-20 w-auto mx-auto mb-6 invert"
            />
            <p className="text-gray-400 text-sm">
              © {new Date().getFullYear()} High Grade Diamonds. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
