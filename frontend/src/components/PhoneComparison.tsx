import { ArrowRight, Check, X } from 'lucide-react';
import type { ComparisonData } from '../types/api.types';

interface PhoneComparisonProps {
  comparison: ComparisonData;
}

export function PhoneComparison({ comparison }: PhoneComparisonProps) {
  const { phone_1, phone_2 } = comparison;

  const ComparisonRow = ({
    label,
    value1,
    value2,
    isBetter1,
    isBetter2,
  }: {
    label: string;
    value1: string | number;
    value2: string | number;
    isBetter1?: boolean;
    isBetter2?: boolean;
  }) => (
    <div className="grid grid-cols-[1fr,auto,1fr] gap-4 items-center py-3 border-b border-gray-100 last:border-0">
      <div
        className={`text-sm text-right ${
          isBetter1 ? 'font-bold text-green-700' : 'text-gray-700'
        }`}
      >
        {value1}
      </div>
      <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide min-w-[120px] text-center">
        {label}
      </div>
      <div
        className={`text-sm text-left ${
          isBetter2 ? 'font-bold text-green-700' : 'text-gray-700'
        }`}
      >
        {value2}
      </div>
    </div>
  );

  return (
    <div className="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
      <div className="bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-600 p-6 text-white">
        <div className="grid grid-cols-[1fr,auto,1fr] gap-4 items-center">
          <div className="text-right">
            <h3 className="text-xl font-bold mb-1">{phone_1.name}</h3>
            <p className="text-blue-100 text-sm">{phone_1.brand}</p>
            <p className="text-2xl font-bold mt-2">₹{phone_1.price.toLocaleString()}</p>
          </div>
          <div className="flex justify-center">
            <div className="bg-white/20 rounded-full p-3">
              <ArrowRight className="w-6 h-6" />
            </div>
          </div>
          <div className="text-left">
            <h3 className="text-xl font-bold mb-1">{phone_2.name}</h3>
            <p className="text-blue-100 text-sm">{phone_2.brand}</p>
            <p className="text-2xl font-bold mt-2">₹{phone_2.price.toLocaleString()}</p>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-1">
        <ComparisonRow
          label="Rating"
          value1={phone_1.rating}
          value2={phone_2.rating}
          isBetter1={phone_1.rating > phone_2.rating}
          isBetter2={phone_2.rating > phone_1.rating}
        />
        <ComparisonRow
          label="Display"
          value1={`${phone_1.display_size_inch}" ${phone_1.display_type}`}
          value2={`${phone_2.display_size_inch}" ${phone_2.display_type}`}
        />
        <ComparisonRow
          label="Refresh Rate"
          value1={`${phone_1.refresh_rate}Hz`}
          value2={`${phone_2.refresh_rate}Hz`}
          isBetter1={phone_1.refresh_rate > phone_2.refresh_rate}
          isBetter2={phone_2.refresh_rate > phone_1.refresh_rate}
        />
        <ComparisonRow
          label="Processor"
          value1={phone_1.processor}
          value2={phone_2.processor}
        />
        <ComparisonRow
          label="RAM"
          value1={`${phone_1.ram_gb}GB`}
          value2={`${phone_2.ram_gb}GB`}
          isBetter1={phone_1.ram_gb > phone_2.ram_gb}
          isBetter2={phone_2.ram_gb > phone_1.ram_gb}
        />
        <ComparisonRow
          label="Storage"
          value1={`${phone_1.storage_gb}GB`}
          value2={`${phone_2.storage_gb}GB`}
          isBetter1={phone_1.storage_gb > phone_2.storage_gb}
          isBetter2={phone_2.storage_gb > phone_1.storage_gb}
        />
        <ComparisonRow
          label="Battery"
          value1={`${phone_1.battery_mah}mAh`}
          value2={`${phone_2.battery_mah}mAh`}
          isBetter1={phone_1.battery_mah > phone_2.battery_mah}
          isBetter2={phone_2.battery_mah > phone_1.battery_mah}
        />
        <ComparisonRow
          label="Charging"
          value1={`${phone_1.charging_speed_w}W`}
          value2={`${phone_2.charging_speed_w}W`}
          isBetter1={phone_1.charging_speed_w > phone_2.charging_speed_w}
          isBetter2={phone_2.charging_speed_w > phone_1.charging_speed_w}
        />
        <ComparisonRow
          label="Rear Camera"
          value1={`${phone_1.rear_camera_mp}MP`}
          value2={`${phone_2.rear_camera_mp}MP`}
          isBetter1={phone_1.rear_camera_mp > phone_2.rear_camera_mp}
          isBetter2={phone_2.rear_camera_mp > phone_1.rear_camera_mp}
        />
        <ComparisonRow
          label="Front Camera"
          value1={`${phone_1.front_camera_mp}MP`}
          value2={`${phone_2.front_camera_mp}MP`}
          isBetter1={phone_1.front_camera_mp > phone_2.front_camera_mp}
          isBetter2={phone_2.front_camera_mp > phone_1.front_camera_mp}
        />
        <ComparisonRow
          label="Weight"
          value1={`${phone_1.weight_g}g`}
          value2={`${phone_2.weight_g}g`}
          isBetter1={phone_1.weight_g < phone_2.weight_g}
          isBetter2={phone_2.weight_g < phone_1.weight_g}
        />
      </div>

      <div className="grid grid-cols-2 gap-4 p-6 bg-gray-50">
        <div>
          <div className="text-sm font-semibold text-gray-700 mb-3">
            {phone_1.name} Highlights
          </div>
          <div className="space-y-2">
            {phone_1.pros.map((pro, idx) => (
              <div key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                <Check className="w-4 h-4 text-green-600 flex-shrink-0 mt-0.5" />
                <span>{pro}</span>
              </div>
            ))}
            {phone_1.cons.map((con, idx) => (
              <div key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                <X className="w-4 h-4 text-red-600 flex-shrink-0 mt-0.5" />
                <span>{con}</span>
              </div>
            ))}
          </div>
        </div>
        <div>
          <div className="text-sm font-semibold text-gray-700 mb-3">
            {phone_2.name} Highlights
          </div>
          <div className="space-y-2">
            {phone_2.pros.map((pro, idx) => (
              <div key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                <Check className="w-4 h-4 text-green-600 flex-shrink-0 mt-0.5" />
                <span>{pro}</span>
              </div>
            ))}
            {phone_2.cons.map((con, idx) => (
              <div key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                <X className="w-4 h-4 text-red-600 flex-shrink-0 mt-0.5" />
                <span>{con}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
