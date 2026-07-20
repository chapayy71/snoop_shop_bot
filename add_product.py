import asyncio

from database.session import async_session
from database.models import Product, Category


async def main():

    async with async_session() as session:

        category = Category(
            name="Табак для кальяна"
        )

        session.add(category)

        await session.flush()


        product = Product(
            name="MustHave Pinkman",
            description="Табак для кальяна MustHave Pinkman 25г",
            price=280,
            stock=5,
            category_id=category.id
        )

        session.add(product)

        await session.commit()


asyncio.run(main())