namespace Demo;
public sealed class OrderService
{
    private readonly PricingService _pricing;
    public decimal CalculateTotal(Order order)
    {
        return _pricing.GetPrice(order.ProductId) * order.Quantity;
    }
}
