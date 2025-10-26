import { Battery, Camera, Cpu, Monitor, Smartphone, Star, TrendingUp } from 'lucide-react';
import type { PhoneDetails } from '../types/api.types';

interface PhoneDetailCardProps {
  phone: PhoneDetails;
}

export function PhoneDetailCard({ phone }: PhoneDetailCardProps) {
  return (
    <div className="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100 hover:shadow-xl transition-shadow">
      <div className="bg-gradient-to-r from-blue-500 to-cyan-500 p-6 text-white">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="text-2xl font-bold mb-1">{phone.name}</h3>
            <p className="text-blue-100 text-sm">{phone.brand}</p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold">₹{phone.price.toLocaleString()}</div>
            <div className="flex items-center gap-1 mt-1 justify-end">
              <Star className="w-4 h-4 fill-yellow-300 text-yellow-300" />
              <span className="text-sm">{phone.rating}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-start gap-3">
            <div className="bg-blue-50 p-2 rounded-lg">
              <Monitor className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <div className="text-xs text-gray-500">Display</div>
              <div className="text-sm font-semibold text-gray-900">
                {phone.display_size_inch}" {phone.display_type}
              </div>
              <div className="text-xs text-gray-600">{phone.refresh_rate}Hz</div>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <div className="bg-green-50 p-2 rounded-lg">
              <Cpu className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <div className="text-xs text-gray-500">Processor</div>
              <div className="text-sm font-semibold text-gray-900">{phone.processor}</div>
              <div className="text-xs text-gray-600">
                {phone.ram_gb}GB + {phone.storage_gb}GB
              </div>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <div className="bg-purple-50 p-2 rounded-lg">
              <Camera className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <div className="text-xs text-gray-500">Camera</div>
              <div className="text-sm font-semibold text-gray-900">{phone.rear_camera_mp}MP</div>
              <div className="text-xs text-gray-600">{phone.front_camera_mp}MP Front</div>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <div className="bg-orange-50 p-2 rounded-lg">
              <Battery className="w-5 h-5 text-orange-600" />
            </div>
            <div>
              <div className="text-xs text-gray-500">Battery</div>
              <div className="text-sm font-semibold text-gray-900">{phone.battery_mah}mAh</div>
              <div className="text-xs text-gray-600">{phone.charging_speed_w}W Charging</div>
            </div>
          </div>
        </div>

        <div>
          <div className="text-xs font-semibold text-gray-700 mb-2">Features</div>
          <div className="flex flex-wrap gap-2">
            {phone.features.map((feature, idx) => (
              <span
                key={idx}
                className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-medium"
              >
                {feature}
              </span>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-xs font-semibold text-green-700 mb-2">Pros</div>
            <ul className="space-y-1">
              {phone.pros.map((pro, idx) => (
                <li key={idx} className="text-xs text-gray-700 flex items-start gap-1">
                  <span className="text-green-600 mt-0.5">✓</span>
                  <span>{pro}</span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <div className="text-xs font-semibold text-red-700 mb-2">Cons</div>
            <ul className="space-y-1">
              {phone.cons.map((con, idx) => (
                <li key={idx} className="text-xs text-gray-700 flex items-start gap-1">
                  <span className="text-red-600 mt-0.5">✗</span>
                  <span>{con}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-gray-100">
          <div className="flex items-center gap-2">
            <Smartphone className="w-4 h-4 text-gray-400" />
            <span className="text-xs text-gray-600">{phone.os}</span>
            <span className="text-gray-300">•</span>
            <span className="text-xs text-gray-600">{phone.network}</span>
            <span className="text-gray-300">•</span>
            <span className="text-xs text-gray-600">{phone.released_year}</span>
          </div>
          <div className="flex items-center gap-1">
            <TrendingUp className="w-4 h-4 text-blue-500" />
            <span className="text-xs font-semibold text-blue-600">
              {phone.popularity_score}/100
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
