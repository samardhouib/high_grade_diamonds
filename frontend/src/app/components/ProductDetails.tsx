'use client'

import Link from 'next/link'
import Image from 'next/image'
import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'

interface Product {
  _id: string
  title: string
  description: string
  images: string[]
  category: string
  subcategory: string
  url: string
  details?: Record<string, any>
}

async function getProduct(id: string): Promise<Product | null> {
  try {
    const res = await fetch(`http://localhost:8000/products/${id}`, {
      cache: 'no-store'
    })
    if (!res.ok) {
      // Check for 404 specifically
      if (res.status === 404) {
        return null
      }
      throw new Error(`Failed to fetch product: ${res.statusText}`)
    }
    return res.json()
  } catch (error) {
    console.error("Error fetching product in client component:", error)
    return null
  }
}

export default function ProductDetails({ id }: { id: string }) {
  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchProductData() {
      try {
        const productData = await getProduct(id)
        setProduct(productData)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unknown error occurred')
      } finally {
        setLoading(false)
      }
    }
    fetchProductData()
  }, [id])

  if (loading) {
    return (
      <div className="min-h-screen bg-lightbg flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-charcoal mx-auto"></div>
          <p className="text-gray-600 mt-4 font-sans">Loading product details...</p>
        </div>
      </div>
    )
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-lightbg flex items-center justify-center">
        <div className="text-center p-8 bg-white shadow-lg rounded-xl border border-borderlight m-4">
          <h1 className="text-3xl font-serif text-charcoal mb-4">Product Not Found</h1>
          <p className="text-gray-700 mb-6 font-sans leading-relaxed">
            {error || 'The product you are looking for does not exist or an error occurred.'}
          </p>
          <Link
            href="/"
            className="inline-flex items-center px-6 py-3 bg-gold text-white rounded-lg hover:bg-gold-700 transition-colors duration-300 text-lg font-medium shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
          >
            ← Back to Home
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <header className="bg-white shadow-lg border-b-2 border-gold sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <Link href="/" className="flex items-center">
              <Image
                src="/images/logo.png"
                alt="HIGH GRADE DIAMONDS"
                width={280}
                height={168}
                className="h-24 w-auto"
                priority
              />
            </Link>
            <div className="flex items-center space-x-4">
              <Link
                href={`/`}
                className="text-charcoal hover:text-gold font-medium transition-colors duration-200 flex items-center uppercase tracking-wider text-sm"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                Back to {product.category}
              </Link>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 bg-white p-8 rounded-xl shadow-lg border border-borderlight">
          {/* Product Images */}
          <div className="space-y-6">
            {product.images && product.images.length > 0 ? (
              <div className="grid grid-cols-1 gap-6">
                {product.images.map((image, index) => (
                  <div
                    key={index}
                    className="relative aspect-square bg-darkbg rounded-lg overflow-hidden border border-borderlight"
                  >
                    <Image
                      src={`/images/${image}`}
                      alt={`${product.title} - Image ${index + 1}`}
                      fill
                      className="object-contain"
                      sizes="(max-width: 1024px) 100vw, 50vw"
                      priority={index === 0}
                    />
                  </div>
                ))}
              </div>
            ) : (
              <div className="aspect-square bg-darkbg rounded-lg flex items-center justify-center border border-borderlight">
                <span className="text-gray-500 font-serif text-lg">No images available</span>
              </div>
            )}
          </div>

          {/* Product Details */}
          <div className="space-y-8">
            <div>
              <h1 className="text-4xl font-serif text-charcoal mb-4">
                {product.title}
              </h1>
              <div className="flex flex-wrap items-center space-x-4 text-sm text-gray-600 mb-6">
                <span className="bg-gold-100 text-gold-800 px-4 py-1 rounded-full font-medium">
                  {product.category}
                </span>
                <span className="bg-teal-100 text-teal-800 px-4 py-1 rounded-full font-medium">
                  {product.subcategory}
                </span>
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-serif text-charcoal mb-4">
                Description
              </h2>
              <p className="text-gray-700 leading-relaxed whitespace-pre-line text-lg">
                {product.description}
              </p>
            </div>

            {product.details && Object.keys(product.details).length > 0 && (
              <div>
                <h2 className="text-2xl font-serif text-charcoal mb-6 border-b-2 border-gold pb-3">
                  Product Specifications
                </h2>
                <div className="space-y-6">
                  {Object.entries(product.details).map(([key, value]) => {
                    if (!value) return null
                    
                    // Parse the value if it's a string with semicolons
                    const parsedValue = typeof value === 'string' && value.includes(';') 
                      ? value.split(';').filter(v => v.trim())
                      : [value]
                    
                    return (
                      <div key={key} className="bg-gradient-to-br from-gray-50 to-white p-6 rounded-lg border border-borderlight shadow-md">
                        <h3 className="font-serif font-semibold text-charcoal mb-4 text-xl flex items-center">
                          <span className="w-1 h-6 bg-gold mr-3"></span>
                          {key}
                        </h3>
                        {Array.isArray(parsedValue) ? (
                          <div className="space-y-2">
                            {parsedValue.map((item, idx) => {
                              const trimmedItem = typeof item === 'string' ? item.trim() : String(item)
                              if (!trimmedItem) return null
                              
                              // Check if item has key-value format
                              if (trimmedItem.includes(':')) {
                                const [itemKey, itemValue] = trimmedItem.split(':', 2)
                                return (
                                  <div key={idx} className="flex flex-wrap gap-2 py-1">
                                    <span className="font-medium text-charcoal min-w-[140px]">{itemKey.trim()}:</span>
                                    <span className="text-gray-700 flex-1">{itemValue.trim() || 'N/A'}</span>
                                  </div>
                                )
                              }
                              return (
                                <p key={idx} className="text-gray-700 text-base leading-relaxed">
                                  {trimmedItem}
                                </p>
                              )
                            })}
                          </div>
                        ) : (
                          <p className="text-gray-700 text-base leading-relaxed">
                            {String(value)}
                          </p>
                        )}
                      </div>
                    )
                  })}
                </div>
              </div>
            )}

            <div className="flex justify-start mt-8">
              <Link
                href={`/contact?product=${encodeURIComponent(product.title)}&id=${product._id}`}
                className="px-6 py-3 bg-gold text-white rounded-lg hover:bg-gold-700 transition-colors duration-200 text-lg font-medium shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
              >
                Buy
              </Link>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
