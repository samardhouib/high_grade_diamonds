import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Fay Jewelry',
  description: 'Beautiful jewelry collection from Fay Jewelry',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={
        `${inter.className} font-sans antialiased bg-lightbg text-charcoal`
      }>
        {children}
      </body>
    </html>
  )
}
