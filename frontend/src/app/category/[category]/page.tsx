import Link from 'next/link'
import Image from 'next/image'
import { Suspense } from 'react'
import ProductsGrid from '../../components/ProductsGrid'

function ProductsGridFallback() {
  return (
    <div className="text-center py-12">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
      <p className="text-gray-600 mt-4">Loading products...</p>
    </div>
  )
}

export default function CategoryPage({
  params,
}: {
  params: { category: string }
}) {
  const decodedCategory = decodeURIComponent(params.category)

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <header className="bg-white shadow-lg border-b-2 border-gold sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <Link href="/" className="flex items-center">
              <Image
                src="/logo.svg"
                alt="HIGH GRADE DIAMONDS"
                width={280}
                height={168}
                className="h-24 w-auto"
                priority
              />
            </Link>
            <div className="flex items-center space-x-4">
              <Link
                href="/"
                className="text-charcoal hover:text-gold font-medium transition-colors duration-200 uppercase tracking-wider text-sm"
              >
                ← Home
              </Link>
              <span className="text-gray-400">|</span>
              <h1 className="text-2xl font-serif text-charcoal">{decodedCategory}</h1>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-serif text-charcoal mb-2">
            {decodedCategory} Collection
          </h2>
          <p className="text-gray-600 font-sans">
            Discover our exquisite {decodedCategory.toLowerCase()} jewelry pieces
          </p>
        </div>
        <Suspense fallback={
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 py-8">
            {[...Array(8)].map((_, idx) => (
              <div key={idx} className="h-64 bg-darkbg animate-pulse rounded-xl border border-borderlight"></div>
            ))}
          </div>
        }>
          <ProductsGrid category={decodedCategory} />
        </Suspense>
      </main>
    </div>
  )
}
