# Ecommerce App Design

- The system should allow the users to search products from a catalog of products based on different filteration criteria like price range, category, company name, etc.
- User should be able to add products to their cart based on different quantity
- User should be able to place the order of the cart and we support later cancelling the order
- System should be capable of telling the user the latest order situation (Hint : State Design Patterns)


Working Requirements

- working code
- In-memory DB
- CLI Interaction


![](assets/Pasted%20image%2020251120232719.png)


Here we need `OR` criteria as well so we cannot use just Chain of Responsibility.

```java
interface Criteria {
    List<Product> satisfyCriteria(List<Product> p);
}

// we can other Filters implementing Criteria

BrandFilter implements Criteria {
    @Override
    List<Product> satisfyCriteria(List<Product> p){
        return p.stream().filter(p1 -> p1.getBrand().equals());
    }
}

/// brand == 'apple' and brand == 'samsung'
class ANDCriteria implements Criteria {
    public ANDCriteria(List<Criteria> criterias) {};
    List<Product> satisfyCriteria(List<Product> p) {
    }
}

/// brand == 'apple' or brand == 'samsung'
class ORCriteria implements Criteria {
    public ORCriteria(List<Criteria> criterias) {};
    List<Product> satisfyCriteria(List<Product> p) {
    }
}

// both can be clubbed with other criteria
// ((price > 10 and price < 1000) or (brand == 'apple' or brand == 'samsung'))

```
